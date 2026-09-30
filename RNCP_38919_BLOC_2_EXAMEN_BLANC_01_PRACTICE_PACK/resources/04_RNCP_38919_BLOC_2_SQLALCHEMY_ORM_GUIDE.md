# 04 — RNCP 38919 — Bloc 2
# Guide SQLAlchemy & ORM

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 2 — Projet ETL & ML  
**Ressource dédiée :** ORM — durée indicative 2h00

**Source principale :**
- `Examen RNCP 38919 _ Bloc 2 - ORM.pdf`

**Source de cadrage :**
- `Examen RNCP 38919 _ Bloc 2 - Projet ETL & ML.pdf`

> **Règle de ce document**
>
> Ce guide suit volontairement le vocabulaire, les exemples et le niveau de détail du support ORM fourni.
> Il ne remplace pas les syntaxes du cours par une autre API SQLAlchemy.
>
> Les sections **Source** correspondent au contenu du support.
> Les sections **Entraînement** proposent seulement des exercices dérivés de ce contenu.

---

# 1. Pourquoi l’ORM est important pour le Bloc 2

## Source

Le sujet de préparation au Bloc 2 annonce explicitement :

```text
L'interfaçage avec une base de données SQL
via SQLAlchemy et l'ORM.
```

Le support dédié est intitulé :

```text
Exercice d'introduction
à la technique de programmation informatique ORM
```

Il est structuré autour de quatre grandes parties :

```text
I. SQLAlchemy
II. Object-Relational Mapping
Relations entre tables
Conclusion
```

Le cours se termine en indiquant que les notions présentées constituent les éléments nécessaires pour passer l’examen et recommande de les manipuler en pratique avant le passage.

---

# 2. SQLAlchemy — définition du support

## Source

Le support présente SQLAlchemy comme une bibliothèque Python permettant, comme `Psycopg`, de se connecter et d’interagir avec des bases de données.

La différence mise en avant dans le cours est que SQLAlchemy permet d’interagir avec plusieurs systèmes de bases de données et cite notamment :

```text
SQLite
PostgreSQL
MySQL & MariaDB
Oracle
Microsoft SQL Server
```

Schéma mental :

```text
Python
  ↓
SQLAlchemy
  ↓
Connecteur / dialecte
  ↓
Base de données
```

---

# 3. Pourquoi passer par SQLAlchemy ?

## Source

Le cours met en avant la capacité de SQLAlchemy à généraliser davantage le code Python entre différents systèmes de bases de données.

Le support insiste également sur le fait que :

```text
les syntaxes SQL
peuvent varier
selon le moteur de base de données
```

Il donne un exemple de différence entre PostgreSQL et MySQL pour une expression conditionnelle.

Le message pédagogique est :

```text
SQL écrit directement
=
plus dépendant du dialecte

ORM / abstraction SQLAlchemy
=
plus transparent côté Python
```

---

# 4. Là où intervient l’ORM

## Source

Après avoir illustré les différences de dialecte SQL, le support introduit :

```text
ORM
=
Object-Relational Mapping
```

Le cours présente l’ORM comme une méthode permettant d’interagir avec la base à travers une syntaxe Python et des classes.

Modèle mental :

```text
Objet / classe Python
        │
        ▼
       ORM
        │
        ▼
Table relationnelle
```

---

# 5. Environnement PostgreSQL du cours

## Source

Avant de manipuler l’ORM, le support démarre une base PostgreSQL avec Docker Compose.

Le fichier montré dans le cours contient deux services :

```text
db
pgadmin
```

Le service PostgreSQL utilise notamment :

```yaml
image: postgres:16-alpine
```

et expose :

```text
5432:5432
```

Le service pgAdmin utilise :

```yaml
image: dpage/pgadmin4
```

et expose :

```text
5050:80
```

Le support montre également des variables d’environnement pour :

```text
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB

PGADMIN_DEFAULT_EMAIL
PGADMIN_DEFAULT_PASSWORD
```

---

# 6. Dépendances installées dans le support

## Source

Le cours installe :

```bash
pip install sqlalchemy psycopg[binary]
```

La connexion présentée utilise donc :

```text
SQLAlchemy
+
Psycopg
+
PostgreSQL
```

---

# 7. Première connexion avec `create_engine`

## Source

Le support importe :

```python
from sqlalchemy import create_engine, text
```

Puis construit un moteur :

```python
engine = create_engine(
    "postgresql+psycopg://daniel:datascientest@localhost:5432/dst_db"
)
```

Le modèle de chaîne de connexion visible est :

```text
postgresql+psycopg://
USER:PASSWORD@HOST:PORT/DATABASE
```

---

# 8. Tester la connexion

## Source

Le cours exécute une requête simple via le moteur :

```python
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT version();")
    )
    print(result.fetchone())
```

Objectif :

```text
valider la connexion
avant de passer à l'ORM
```

---

# 9. ORM : le « O » signifie objet

## Source

Le support explique que :

```text
O de ORM = Object
```

et rattache l’objet à la notion de :

```text
classe Python
```

Le changement de modèle mental est donc :

```text
Avant
─────
écrire une requête SQL

ORM
───
manipuler des classes / objets Python
```

---

# 10. Les deux éléments nécessaires selon le cours

## Source

Pour créer une table avec l’approche présentée, le support distingue :

```text
1. la base
2. l'objet / la classe représentant la table
```

---

# 11. Définir la base déclarative

## Source

Le cours utilise :

```python
from sqlalchemy.orm import declarative_base

Base = declarative_base()
```

Dans le support :

```text
Base
```

est le socle dont héritent les classes représentant les tables.

---

# 12. Types et colonnes

## Source

Le cours introduit notamment :

```text
Column
Integer
String
```

avec les rôles suivants :

```text
Column
→ désigne une colonne

Integer
→ entier

String
→ chaîne de caractères
```

Import :

```python
from sqlalchemy import Column, Integer, String
```

---

# 13. `__tablename__`

## Source

Le support indique que le nom de la table est défini avec :

```python
__tablename__
```

Exemple :

```python
class User(Base):
    __tablename__ = "users"
```

---

# 14. Clé primaire

## Source

Le cours utilise le paramètre :

```python
primary_key=True
```

Exemple :

```python
id = Column(
    Integer,
    primary_key=True,
)
```

---

# 15. Premier modèle ORM complet

## Source

Le modèle présenté dans le support est équivalent à :

```python
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
    )

    user = Column(String)
```

Correspondance mentale :

```text
class User
   ↓
table users

id
   ↓
INTEGER PRIMARY KEY

user
   ↓
STRING
```

---

# 16. Créer les tables

## Source

Le support utilise :

```python
Base.metadata.create_all(engine)
```

Il montre également une création ciblée :

```python
Base.metadata.create_all(
    engine,
    tables=[User.__table__],
)
```

Le cours précise que lorsqu’une table particulière est ciblée, il faut fournir :

```python
User.__table__
```

et non directement :

```python
User
```

---

# 17. `checkfirst`

## Source

Le support illustre explicitement :

```python
Base.metadata.create_all(
    engine,
    checkfirst=True,
)
```

puis compare ce comportement à :

```python
Base.metadata.create_all(
    engine,
    checkfirst=False,
)
```

Dans l’exercice, `checkfirst=True` est utilisé pour éviter un conflit lorsqu’une table existe déjà.

> Ce guide conserve exactement l’approche présentée dans le support et recommande d’être explicite sur `checkfirst=True` pendant les exercices de préparation.

---

# 18. Supprimer les tables

## Source

Le cours indique que l’opération correspondante est :

```python
Base.metadata.drop_all(...)
```

Exemple de révision :

```python
Base.metadata.drop_all(
    engine,
)
```

Attention :

```text
DROP
=
opération destructive
```

---

# 19. Créer une session

## Source

Le support introduit :

```python
sessionmaker
```

Import :

```python
from sqlalchemy.orm import sessionmaker
```

Création :

```python
Session = sessionmaker(
    bind=engine
)

session = Session()
```

Modèle mental :

```text
engine
  ↓
Session factory
  ↓
session
  ↓
opérations ORM
```

---

# 20. Créer un objet

## Source

Le support crée un utilisateur :

```python
new_user = User(
    id=37,
    user="Nintri",
)
```

Ici :

```text
new_user
```

est un objet Python représentant une ligne destinée à la table :

```text
users
```

---

# 21. Ajouter et valider

## Source

Insertion :

```python
session.add(new_user)
session.commit()
```

À mémoriser :

```text
add()
  ↓
commit()
```

---

# 22. Lire toutes les lignes

## Source

Le cours utilise :

```python
users = session.query(User).all()
```

puis :

```python
for user in users:
    print(
        user.id,
        user.user,
    )
```

Le résultat illustré contient notamment :

```text
37 Nintri
```

---

# 23. Auto-génération de l’identifiant

## Source

Le support crée ensuite un nouvel utilisateur sans fournir explicitement `id` :

```python
new_user = User(
    user="Emperor",
)
```

puis :

```python
session.add(new_user)
session.commit()
```

Le cours montre que l’identifiant est alors attribué lors de l’insertion.

Réflexe :

```text
si la PK est gérée par la base,
ne pas fabriquer manuellement
tous les IDs
```

lorsque le modèle le permet.

---

# 24. Filtrer

## Source

Le support présente :

```python
session.query(User).filter_by(
    id=1
).all()
```

Exemple condensé :

```python
user_1 = (
    session
    .query(User)
    .filter_by(id=1)
    .all()
)
```

Le cours précise qu’il existe d’autres opérations mais que l’objectif de cette ressource est introductif.

---

# 25. Ce qu’il faut vraiment maîtriser pour l’examen

## Source dérivée du périmètre du support

```text
create_engine
declarative_base
Column
Integer
String
__tablename__
primary_key
create_all
sessionmaker
add
commit
query
all
filter_by
ForeignKey
relationship
```

Le support ne cherche pas à couvrir l’intégralité de SQLAlchemy.

---

# 26. Relations entre tables

## Source

La dernière grande partie du support est :

```text
Relations entre tables
```

Le cours rappelle qu’une base relationnelle nécessite des relations pour rendre les tables cohérentes entre elles.

Pour créer cette relation, le support introduit :

```text
clé étrangère
+
relationship
```

---

# 27. Imports relationnels

## Source

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
```

---

# 28. Table `Address`

## Source

Le modèle présenté est équivalent à :

```python
class Address(Base):
    __tablename__ = "addresses"

    id = Column(
        Integer,
        primary_key=True,
    )

    email = Column(String)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
    )

    user = relationship("User")
```

---

# 29. Comprendre `ForeignKey`

## Source + synthèse

```python
ForeignKey("users.id")
```

signifie :

```text
addresses.user_id
        │
        ▼
    users.id
```

Modèle :

```text
users
────────────
id PK
user
   │
   │ 1
   │
   ▼ N
addresses
────────────
id PK
email
user_id FK
```

---

# 30. Comprendre `relationship`

## Source

Le cours utilise :

```python
user = relationship("User")
```

Le rôle présenté est de relier l’objet `Address` à l’objet `User` côté ORM.

Résumé :

```text
ForeignKey
→ lien dans la base

relationship
→ navigation entre objets ORM
```

---

# 31. Créer les nouvelles tables

## Source

Après définition de `Address`, le support appelle :

```python
Base.metadata.create_all(
    engine,
    checkfirst=True,
)
```

---

# 32. Insérer un utilisateur puis son adresse

## Source

Le support procède dans cet ordre :

```python
u = User(
    user="Nintri"
)

session.add(u)
session.commit()
```

puis :

```python
a = Address(
    email="nintri@example.com",
    user=u,
)

session.add(a)
session.commit()
```

Le point important est :

```text
créer d'abord le User
puis créer l'Address liée
```

dans l’exemple pédagogique fourni.

---

# 33. Vérifier les données

## Source

Le support interroge d’abord les utilisateurs :

```python
all_users = (
    session
    .query(User)
    .all()
)
```

puis les adresses :

```python
all_addresses = (
    session
    .query(Address)
    .all()
)
```

et affiche notamment :

```python
address.id
address.email
address.user_id
```

afin de vérifier que la clé étrangère est bien renseignée.

---

# 34. `__table_args__` et table déjà existante

## Source

Le support montre enfin :

```python
__table_args__ = {
    "extend_existing": True
}
```

pour étendre la définition lorsqu’une classe représentant une table existe déjà dans le contexte de l’exercice.

Ce point apparaît en fin de support et reste secondaire par rapport à :

```text
PK
FK
session
insert
query
relationship
```

---

# 35. Architecture mentale complète

```text
PostgreSQL
   ▲
   │
Engine
   ▲
   │
SQLAlchemy
   ▲
   │
Base = declarative_base()
   │
   ├──────────────┐
   ▼              ▼
 User          Address
   │              │
   │              ├── ForeignKey
   │              └── relationship
   │
   ▼
Session
   │
   ├── add
   ├── commit
   ├── query
   └── filter_by
```

---

# 36. Code complet basé sur le support

## Entraînement

```python
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
)


DATABASE_URL = (
    "postgresql+psycopg://"
    "daniel:datascientest"
    "@localhost:5432/dst_db"
)


engine = create_engine(
    DATABASE_URL
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
    )

    user = Column(String)


class Address(Base):
    __tablename__ = "addresses"

    id = Column(
        Integer,
        primary_key=True,
    )

    email = Column(String)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
    )

    user = relationship("User")


Base.metadata.create_all(
    engine,
    checkfirst=True,
)


Session = sessionmaker(
    bind=engine
)

session = Session()


u = User(
    user="Nintri"
)

session.add(u)
session.commit()


a = Address(
    email="nintri@example.com",
    user=u,
)

session.add(a)
session.commit()


users = session.query(User).all()

for user in users:
    print(
        user.id,
        user.user,
    )


addresses = (
    session
    .query(Address)
    .all()
)

for address in addresses:
    print(
        address.id,
        address.email,
        address.user_id,
    )
```

---

# 37. Pattern à reconstruire de mémoire

```python
engine = create_engine(URL)

Base = declarative_base()


class Model(Base):
    __tablename__ = "table"

    id = Column(
        Integer,
        primary_key=True,
    )


Base.metadata.create_all(
    engine,
    checkfirst=True,
)

Session = sessionmaker(
    bind=engine
)

session = Session()

obj = Model(...)

session.add(obj)
session.commit()

rows = session.query(Model).all()
```

---

# 38. Passage d’un schéma métier à l’ORM

## Entraînement

Avant de coder :

```text
1. Identifier les entités
2. Identifier les tables
3. Définir le grain
4. Définir la PK
5. Identifier les relations
6. Définir les FK
7. Écrire les classes
8. create_all
9. session
10. ingestion
```

---

# 39. Exemple de raisonnement

Besoin :

```text
Un utilisateur peut avoir plusieurs adresses.
```

Traduction :

```text
User
1
│
N
Address
```

Tables :

```text
users
─────
id PK
user

addresses
─────────
id PK
email
user_id FK → users.id
```

ORM :

```python
user_id = Column(
    Integer,
    ForeignKey("users.id"),
)

user = relationship("User")
```

---

# 40. Relier l’ETL précédent à l’ORM

Le document `03` produisait :

```text
JSON
 ↓
pandas DataFrame propre
```

La suite devient :

```text
DataFrame propre
 ↓
boucle / mapping
 ↓
objets ORM
 ↓
session.add(...)
 ↓
session.commit()
 ↓
PostgreSQL
```

---

# 41. Pattern d’ingestion depuis pandas

## Entraînement dérivé

```python
def ingest_users(
    df,
    session,
):
    for _, row in df.iterrows():
        user = User(
            user=row["user"]
        )

        session.add(user)

    session.commit()
```

Le support ne fournit pas ce code exact ; il dérive directement des opérations `User(...)`, `session.add()` et `session.commit()` présentées dans le cours.

---

# 42. Variante avec relations

## Entraînement dérivé

```python
user = User(
    user="Alice"
)

session.add(user)
session.commit()

address = Address(
    email="alice@example.com",
    user=user,
)

session.add(address)
session.commit()
```

Pattern :

```text
Parent
  ↓
commit
  ↓
Child(parent=parent)
  ↓
commit
```

C’est le même ordre que l’exemple `User` → `Address` du support.

---

# 43. Erreurs conceptuelles à éviter

## 1. Oublier `__tablename__`

```python
class User(Base):
    __tablename__ = "users"
```

---

## 2. Oublier la clé primaire

```python
id = Column(
    Integer,
    primary_key=True,
)
```

---

## 3. Définir une FK vers le mauvais nom

Correct selon l’exemple :

```python
ForeignKey("users.id")
```

Le format vise :

```text
nom_table.nom_colonne
```

---

## 4. Ajouter sans valider

```python
session.add(obj)
```

n’est pas la fin du workflow montré.

Le support utilise ensuite :

```python
session.commit()
```

---

## 5. Confondre `ForeignKey` et `relationship`

```text
ForeignKey
→ contrainte de la table

relationship
→ association côté objets Python
```

---

# 44. Debug — connexion

Checklist :

```text
PostgreSQL est-il démarré ?
Le port 5432 est-il exposé ?
Le user est-il correct ?
Le password est-il correct ?
La database existe-t-elle ?
psycopg est-il installé ?
SQLAlchemy est-il installé ?
```

Test minimal issu du support :

```python
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT version();")
    )
    print(result.fetchone())
```

---

# 45. Debug — création de table

Checklist :

```text
Base créée ?
Classe hérite de Base ?
__tablename__ présent ?
PK présente ?
create_all exécuté ?
engine correct ?
checkfirst explicitement défini ?
```

---

# 46. Debug — insertion

Checklist :

```text
session créée ?
objet instancié ?
session.add(obj) ?
session.commit() ?
contrainte FK respectée ?
```

---

# 47. Debug — relation

Checklist :

```text
table parent créée ?
table enfant créée ?
ForeignKey("parent.id") correcte ?
relationship("Parent") correcte ?
parent inséré ?
commit effectué ?
objet enfant lié au bon parent ?
```

---

# 48. Mini-exercice 1 — Connexion

## Entraînement

Objectif :

```text
démarrer PostgreSQL
installer SQLAlchemy + Psycopg
créer engine
exécuter SELECT version()
```

Critère :

```text
la version PostgreSQL s’affiche
```

---

# 49. Mini-exercice 2 — Table simple

Créer :

```text
Product
```

avec :

```text
id
name
```

Puis :

```text
create_all
insert
query all
```

---

# 50. Mini-exercice 3 — Auto-ID

Créer un produit sans fournir `id`.

Vérifier ensuite :

```python
products = (
    session
    .query(Product)
    .all()
)
```

et afficher :

```text
id
name
```

---

# 51. Mini-exercice 4 — Filtre

Insérer plusieurs utilisateurs.

Récupérer uniquement :

```text
id = 1
```

avec :

```python
filter_by(...)
```

---

# 52. Mini-exercice 5 — Relation 1-N

Créer :

```text
Customer
1
│
N
Order
```

Puis traduire en :

```python
ForeignKey(...)
relationship(...)
```

---

# 53. Mini-exercice 6 — ETL → ORM

À partir d’un petit `DataFrame` :

```text
id
user
```

Créer les objets :

```python
User(...)
```

et les insérer dans PostgreSQL.

Objectif :

```text
JSON
→ pandas
→ ORM
→ PostgreSQL
```

---

# 54. Mini-exercice 7 — Relation depuis données

Dataset :

```text
users.json
addresses.json
```

Construire :

```text
User
1
│
N
Address
```

Ordre recommandé d’après le cours :

```text
1. utilisateurs
2. commit
3. adresses liées
4. commit
```

---

# 55. Questions flash

1. À quoi sert SQLAlchemy dans le support ?
2. Pourquoi le cours introduit-il l’ORM ?
3. Quel rôle joue `create_engine()` ?
4. À quoi sert `declarative_base()` ?
5. Que fait `__tablename__` ?
6. Comment déclarer une PK ?
7. Comment créer les tables ?
8. À quoi sert `sessionmaker()` ?
9. Quelle séquence permet d’insérer ?
10. Comment récupérer toutes les lignes ?
11. Comment filtrer avec la syntaxe du cours ?
12. À quoi sert `ForeignKey` ?
13. À quoi sert `relationship` ?
14. Comment lier `Address` à `User` ?
15. Comment vérifier la connexion au moteur ?

---

# 56. Réponses flash

```text
1. Interagir avec des bases via Python et abstraire une partie des différences de moteur.
2. Travailler avec des classes / objets plutôt que tout écrire en SQL direct.
3. Construire le moteur de connexion.
4. Créer la base déclarative des modèles.
5. Définir le nom de table.
6. primary_key=True.
7. Base.metadata.create_all(...).
8. Créer la fabrique de sessions.
9. objet → add → commit.
10. session.query(Model).all().
11. filter_by(...).
12. Déclarer une relation de clé étrangère en base.
13. Représenter / naviguer la relation côté ORM.
14. user_id = ForeignKey("users.id") + relationship("User").
15. engine.connect() + SELECT version().
```

---

# 57. Cheatsheet 30 secondes

```python
engine = create_engine(URL)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
    )

    user = Column(String)


Base.metadata.create_all(
    engine,
    checkfirst=True,
)

Session = sessionmaker(
    bind=engine
)

session = Session()

u = User(user="Alice")

session.add(u)
session.commit()

rows = session.query(User).all()
```

Relation :

```python
user_id = Column(
    Integer,
    ForeignKey("users.id"),
)

user = relationship("User")
```

---

# 58. Ce que le support dit sur la documentation

## Source

La conclusion du support indique que :

```text
la documentation restera accessible
```

tout en recommandant de prendre en main les notions avant l’examen pour gagner du temps.

Le bon objectif n’est donc pas :

```text
mémoriser chaque option SQLAlchemy
```

mais :

```text
connaître le chemin principal
et savoir retrouver rapidement
un détail secondaire
```

---

# 59. Ordre de maîtrise recommandé

```text
NIVEAU 1
create_engine
Base
Model
Column
PK

      ↓

NIVEAU 2
create_all
Session
add
commit
query

      ↓

NIVEAU 3
filter_by
ForeignKey
relationship

      ↓

NIVEAU 4
DataFrame
→ objets ORM
→ ingestion
```

---

# 60. Checkpoint avant de passer à Docker

Être capable, sans recopier le support, de reconstruire :

```text
[ ] engine PostgreSQL
[ ] Base
[ ] User
[ ] Address
[ ] PK
[ ] FK
[ ] relationship
[ ] create_all
[ ] Session
[ ] add
[ ] commit
[ ] query
[ ] filter_by
```

Si cette chaîne est fluide, la partie ORM de préparation est couverte au niveau présenté dans la ressource DataScientest.

---

# 61. Résumé final

Le support ORM du Bloc 2 enseigne essentiellement la progression suivante :

```text
SQLAlchemy
   ↓
Connexion PostgreSQL
   ↓
ORM
   ↓
Base déclarative
   ↓
Classes = tables
   ↓
Colonnes / types / PK
   ↓
create_all
   ↓
Session
   ↓
add / commit
   ↓
query / filter
   ↓
ForeignKey
   ↓
relationship
```

Le point décisif pour l’épreuve est de savoir transformer rapidement :

```text
un schéma relationnel
```

en :

```text
classes SQLAlchemy fonctionnelles
```

puis :

```text
ingérer et relire des données.
```

---

# 62. Document suivant

```text
05_RNCP_38919_BLOC_2_DOCKER_COMPOSE_GUIDE.md
```

Objectif :

> approfondir la partie conteneurisation explicitement annoncée dans le Bloc 2 :
> base relationnelle sous Docker, variables d’environnement, volumes, `docker-compose`
> et environnement de collecte / ingestion.
