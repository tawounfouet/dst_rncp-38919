# LAB 04 — Guide débutant (de zéro à la solution)

> **Public** : tu ne connais ni SQLAlchemy ni la notion d'ORM. On explique tout.
> **Prérequis** : avoir démarré la base du **LAB 03** (`docker compose up -d`).

À la fin, tu auras créé deux tables, inséré des lignes et relu les données,
**sans écrire une seule requête SQL**.

---

## Étape 0 — Le vocabulaire

| Mot | Signification simple |
|---|---|
| **Base de données relationnelle** | Un ensemble de **tables** liées entre elles (comme des feuilles Excel). |
| **Table** | Une grille : colonnes (champs) × lignes (enregistrements). |
| **ORM** | *Object-Relational Mapping* : écrire des **objets Python** qui deviennent des lignes de table. |
| **SQLAlchemy** | La bibliothèque Python qui fait cet ORM. |
| **Modèle** | Une classe Python qui décrit une table (`Customer`, `Delivery`). |
| **PK** (Primary Key) | La colonne qui **identifie de façon unique** une ligne. |
| **FK** (Foreign Key) | Une colonne qui **pointe vers la PK d'une autre table** (le lien). |
| **Session** | Le « carnet de commandes » : on y ajoute des objets, puis on `commit`. |
| **engine** | La **connexion** à la base. |

La relation modélisée ici :

```text
Customer 1 ──── N Delivery
un client  ──── a plusieurs livraisons
```

---

## Étape 1 — Où sont les mots de passe ?

Ils ne sont **pas** dans le code. On les lit depuis le `.env` du LAB 03.

Copie le modèle d'environnement dans le dossier du lab :

```bash
cd LAB_04_SQLALCHEMY_ORM
cp .env.example .env
# si tu as changé le port dans le LAB 03, mets la même valeur ici : DB_PORT=3307
```

`config.py` lit ces variables :

```python
import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "practice")
DB_USER = os.getenv("DB_USER", "practice_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "practice_password")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
```

- `load_dotenv()` → lit le fichier `.env` et met les valeurs dans l'environnement.
- `os.getenv("DB_PORT", "3306")` → lit la variable `DB_PORT` ; si absente, utilise `"3306"` par défaut.
- `DATABASE_URL` → une **chaîne de connexion** au format `driver://user:pass@hote:port/base`.
  - `mysql+pymysql` → on parle à MySQL/MariaDB via le driver `pymysql`.
  - **Ce fichier évite d'écrire les identifiants en dur dans `demo_session.py`.**

`pip install pymysql python-dotenv` si besoin (déjà dans `requirements.txt`).

---

## Étape 2 — Décrire les tables (les modèles)

Fichier `models.py` :

```python
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
```

- `declarative_base()` → on crée une **classe mère** `Base`. Tous nos modèles en hériteront ; SQLAlchemy s'en sert pour connaître les tables.
- `Column`, `Integer`, `String`, `Float`, `ForeignKey` → les **types de colonnes**.
- `relationship` → décrit le **lien** entre deux tables au niveau Python.

Le client :

```python
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    customer_city = Column(String(100), nullable=False)

    deliveries = relationship("Delivery", back_populates="customer")
```

- `class Customer(Base)` → le modèle hérite de `Base` → SQLAlchemy sait que c'est une table.
- `__tablename__ = "customers"` → le **nom réel** de la table en base.
- `customer_id = Column(Integer, primary_key=True)` → colonne entière, **clé primaire** (identifiant unique).
- `customer_city = Column(String(100), nullable=False)` → texte de 100 caractères **obligatoire** (`nullable=False` = interdit d'être vide).
- `relationship("Delivery", back_populates="customer")` → côté Python, `customer.deliveries` donne la liste de ses livraisons. `back_populates` fait le lien avec l'autre côté.

La livraison :

```python
class Delivery(Base):
    __tablename__ = "deliveries"

    delivery_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    vehicle_type = Column(String(50), nullable=False)
    distance_km = Column(Float, nullable=False)
    traffic_level = Column(String(50), nullable=False)
    weather = Column(String(50), nullable=False)
    delivery_minutes = Column(Integer, nullable=False)
    late_delivery = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="deliveries")
```

- `ForeignKey("customers.customer_id")` → **clé étrangère** : `deliveries.customer_id` doit correspondre à un `customer_id` existant dans `customers`. C'est **le lien** entre les tables.
- `relationship("Customer", back_populates="deliveries")` → l'autre côté : `delivery.customer` donne le client de cette livraison.

**Différence PK / FK / relationship :**

```text
PK            → identifie une ligne (clé primaire)
FK            → lien vers la PK d'une autre table (contrainte en base)
relationship  → confort en Python pour naviguer (client.deliveries)
```

---

## Étape 3 — Créer les tables et insérer

Fichier `demo_session.py` :

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL
from models import Base, Customer, Delivery


def main() -> None:
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine, checkfirst=True)
```

- `create_engine(DATABASE_URL)` → prépare la **connexion** (rien n'est encore envoyé).
- `Base.metadata.create_all(engine, checkfirst=True)` → crée les tables décrites par nos modèles. `checkfirst=True` = ne recrée pas si elles existent déjà.

La session :

```python
    Session = sessionmaker(bind=engine)
    session = Session()
```

- `sessionmaker(bind=engine)` → une « fabrique » de sessions liée à notre base.
- `session = Session()` → on ouvre une session (comme ouvrir une transaction).

Insérer un client :

```python
    customer = Customer(customer_id=1, customer_city="paris")
    session.merge(customer)
```

- `Customer(...)` → on crée un **objet Python** avec des attributs (comme un dictionnaire).
- `session.merge(customer)` → « insère ou mets à jour ». `merge` rend le script **réexécutable** : relancé, il ne plante pas avec un doublon de clé (contrairement à `add`).

Insérer une livraison :

```python
    delivery = Delivery(
        delivery_id=1,
        customer_id=1,
        vehicle_type="bike",
        distance_km=4.2,
        traffic_level="high",
        weather="rain",
        delivery_minutes=38,
        late_delivery=1,
    )
    session.merge(delivery)
    session.commit()
```

- `session.commit()` → **valide** et écrit réellement en base. Sans `commit`, rien n'est enregistré.

Relire :

```python
    print(session.query(Customer).all())
    print(session.query(Delivery).all())

    session.close()
```

- `session.query(Customer).all()` → **équivalent de `SELECT * FROM customers`**, mais en Python.
- `session.close()` → ferme proprement la session.

```python
if __name__ == "__main__":
    main()
```

Garde classique : `main()` ne se lance que si on exécute ce fichier directement.

---

## Étape 4 — Exécuter et vérifier

**1. La base du LAB 03 doit tourner :**

```bash
cd ../LAB_03_DOCKER_COMPOSE_DB/solution
cp .env.example .env && docker compose up -d && docker compose ps
```

**2. Lancer la démo :**

```bash
cd ../../LAB_04_SQLALCHEMY_ORM/solution
python demo_session.py
```

Attendu :

```text
[<models.Customer object at 0x...>]
[<models.Delivery object at 0x...>]
```

**3. Vérifier en base :**

```bash
cd ../../LAB_03_DOCKER_COMPOSE_DB/solution
docker compose exec db mariadb -upractice_user -ppractice_password practice \
  -e "SELECT * FROM customers; SELECT * FROM deliveries;"
```

Tu dois voir la ville `paris` et la livraison `bike`.

Relance `python demo_session.py` : **toujours 1 ligne** (pas de doublon) grâce à `merge`.

---

## Erreurs fréquentes

| Message | Cause | Solution |
|---|---|---|
| `Access denied for user` | mot de passe ou **port** différent du LAB 03 | aligne `.env` (surtout `DB_PORT`) |
| `Can't connect ... (111)` | base pas démarrée | `docker compose up -d` dans le LAB 03 |
| `ModuleNotFoundError: models` | lancé depuis un autre dossier | `cd solution` avant de lancer |
| `ModuleNotFoundError: dotenv` | dépendance manquante | `pip install -r ../requirements.txt` |
| `Duplicate entry '1' for key 'PRIMARY'` | `add` au lieu de `merge` | utiliser `merge` (script réexécutable) |

---

## Mini-glossaire final

```text
ORM          → objets Python qui deviennent des lignes de table
Base         → classe mère des modèles
Column       → une colonne de table
primary_key  → identifiant unique
ForeignKey   → lien vers une autre table
relationship → navigation Python entre objets liés
engine       → connexion à la base
Session      → carnet de commandes (add/merge puis commit)
create_all   → crée les tables depuis les modèles
```
