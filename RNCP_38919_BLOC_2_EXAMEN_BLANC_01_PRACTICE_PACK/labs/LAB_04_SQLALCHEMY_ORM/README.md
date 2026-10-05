# LAB 04 — SQLAlchemy ORM

**Temps cible : 35 min** · Difficulté : ⭐⭐⭐ · Prérequis : **LAB 03 (DB démarrée)**

## Objectifs

Modéliser une relation **1‑N** et persister via une session :

```text
Customer 1 ──< N Delivery
```

## Contenu

```text
LAB_04_SQLALCHEMY_ORM/
├── starter/
│   └── models.py        # Customer / Delivery à compléter (TODO)
├── solution/
│   ├── config.py        # DATABASE_URL depuis .env
│   ├── models.py        # Base, Customer, Delivery
│   └── demo_session.py  # main() : create_all + merge + query
├── .env.example
├── EXO.md
└── README.md
```

## Lancement

**1. Démarrer la base (LAB 03) :**

```bash
cd ../LAB_03_DOCKER_COMPOSE_DB/solution
cp .env.example .env
docker compose up -d
docker compose ps          # attendre que db soit Up
```

**2. Configurer puis lancer le LAB 04 :**

```bash
cd ../../LAB_04_SQLALCHEMY_ORM
cp .env.example .env
# si vous avez changé DB_PORT dans le LAB 03, alignez-le ici
cd solution
python demo_session.py
```

Sortie attendue :

```text
[<models.Customer object at 0x...>]
[<models.Delivery object at 0x...>]
```

Vérification en base :

```bash
cd ../../LAB_03_DOCKER_COMPOSE_DB/solution
docker compose exec db mariadb -upractice_user -ppractice_password practice -e "SELECT * FROM customers; SELECT * FROM deliveries;"
```

## API à utiliser

`create_engine` · `declarative_base` · `Column` · `Integer` · `String` · `Float`
· `ForeignKey` · `relationship` · `sessionmaker` · `create_all` · `add` · `commit`
· `query`

## Critères de réussite

- [ ] `demo_session.py` se termine sans erreur ;
- [ ] les tables `customers` et `deliveries` existent en base ;
- [ ] une ligne est insérée dans chacune ;
- [ ] relancer le script **ne crée pas** de doublon (idempotence via `merge`) ;
- [ ] `Delivery.customer` et `Customer.deliveries` sont cohérents (relation).

## Dépannage

| Symptôme | Cause | Correctif |
|---|---|---|
| `Access denied for user 'practice_user'@'localhost'` | mot de passe ou **port** différents du LAB 03 | aligner `.env` (surtout `DB_PORT`) ; le défaut `3306` peut aussi viser un autre MySQL local |
| `Can't connect ... (111)` | DB pas démarrée | relancer `docker compose up -d` dans le LAB 03 |
| `ModuleNotFoundError: models` | lancé depuis un autre dossier | `cd solution` avant `python demo_session.py` |
| `ModuleNotFoundError: dotenv` | dépendance manquante | `pip install -r ../requirements.txt` |
| `Duplicate entry '1' for key 'PRIMARY'` | ancienne version du script (avant correctif) | la solution utilise `session.merge` → réexécutable |
| table `deliveries` absente | `create_all` non appelé | vérifier `Base.metadata.create_all(engine)` |

> **Note correctif :** `demo_session.py` lisait auparavant une URL **codée en dur
> sur le port 3306**, ce qui cassait dès que `DB_PORT` changeait dans le LAB 03.
> Il passe désormais par `config.py` (`.env`) et utilise `merge` (idempotent).

## Pour aller plus loin

- Ajouter une contrainte `UniqueConstraint` et gérer le `IntegrityError`.
- Écrire une requête de jointure : nombre de livraisons par ville.
- Passer à une gestion de sessions avec `with Session() as session:`.
