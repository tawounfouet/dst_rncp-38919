# 01 — RNCP 38919 — Bloc 2
# Fiche de révision

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 2 — Projet ETL & ML  
**Durée officielle :** 4 heures  
**Ressource complémentaire :** ORM — 2 heures

**Sources de cette fiche :**
- `Examen RNCP 38919 _ Bloc 2 - Projet ETL & ML.pdf`
- `Examen RNCP 38919 _ Bloc 2 - ORM.pdf`
- `Consignes surveillance évaluation.pdf`

> **Convention de lecture**
>
> - **Source** = élément explicitement présent dans les supports fournis.
> - **Réflexe de révision** = synthèse ou exemple pratique proposé pour préparer l’épreuve ; ce n’est pas une consigne supplémentaire de DataScientest.

---

# 1. Le Bloc 2 en une page

## Source

L’épreuve principale dure :

```text
4 heures
```

et se déroule :

```text
EN DIRECT avec Learn + Mereos
```

Le support de préparation annonce un mini-projet couvrant notamment :

```text
JSON
Jupyter
Python
pandas
matplotlib
valeurs manquantes
colonnes catégorielles
base de données relationnelle
Docker
variables d’environnement
schéma logique
PK / FK
SQLAlchemy
ORM
scikit-learn
joblib
docker-compose
tests d’ingestion
impact écologique
```

Le rendu doit notamment comporter :

```text
notebook d’exploration
script extraction / transformation
script de création de base via ORM
script d’ingestion
script d’entraînement ML
fichier synthétique sur l’architecture,
les choix techniques et les pistes d’amélioration
```

---

# 2. Modèle mental à retenir

## Réflexe de révision

```text
JSON
  ↓
Jupyter
  ↓
Comprendre les données
  ↓
pandas
  ↓
Nettoyer / transformer
  ↓
Modéliser les tables
  ↓
SQLAlchemy ORM
  ↓
Créer la base
  ↓
Ingérer
  ↓
Préparer X / y
  ↓
scikit-learn
  ↓
Évaluer
  ↓
joblib
  ↓
docker-compose
  ↓
Tests
  ↓
Documentation
  ↓
ZIP FINAL
```

Le principe de préparation est simple :

> savoir faire fonctionner toute la chaîne sans rester bloqué longtemps sur une seule brique.

---

# 3. Thème 1 — Exploration JSON avec Jupyter

## Source

Le sujet annonce :

```text
exploration de données au format JSON
à l’aide de notebooks Jupyter
```

## À savoir expliquer

- qu’est-ce qu’un fichier JSON ;
- comment est structurée la donnée ;
- quel est le grain d’un enregistrement ;
- quelles colonnes sont exploitables ;
- quelles colonnes comportent des valeurs manquantes ;
- quelles variables peuvent être utiles pour la suite.

## Réflexe de révision

### Chargement simple

```python
import pandas as pd

df = pd.read_json("data.json")
```

### Inspection

```python
df.head()
df.shape
df.columns
df.info()
df.describe(include="all")
```

### Valeurs manquantes

```python
df.isna().sum()
```

### Cardinalité

```python
df.nunique()
```

### Réflexe examen

Avant toute transformation :

```text
1. taille
2. colonnes
3. types
4. nulls
5. doublons
6. target éventuelle
```

---

# 4. Thème 2 — Scripts Python structurés et réutilisables

## Source

Le support annonce :

```text
développement de scripts Python
structurés et réutilisables
```

## À savoir expliquer

La différence entre :

```text
exploration
```

et :

```text
code réutilisable
```

## Réflexe de révision

Passer rapidement de :

```python
df = pd.read_json(...)
df = ...
df.to_csv(...)
```

à :

```python
def extract(path):
    ...

def transform(df):
    ...

def load(df):
    ...
```

### Structure minimale

```python
def main():
    df = extract("data.json")
    df = transform(df)
    load(df)


if __name__ == "__main__":
    main()
```

### À retenir

```text
une fonction
=
une responsabilité claire
```

---

# 5. Thème 3 — pandas et matplotlib

## Source

Le sujet cite explicitement :

```text
pandas
matplotlib
```

## pandas — réflexes de révision

### Sélection

```python
df["column"]
df[["a", "b"]]
```

### Filtre

```python
df[df["age"] > 18]
```

### Tri

```python
df.sort_values("score", ascending=False)
```

### Agrégation

```python
df.groupby("category")["value"].mean()
```

### Renommage

```python
df = df.rename(columns={"old": "new"})
```

### Types

```python
df["age"] = pd.to_numeric(df["age"], errors="coerce")
```

### Doublons

```python
df.duplicated().sum()
df.drop_duplicates()
```

## matplotlib — réflexe de révision

```python
import matplotlib.pyplot as plt

df["value"].hist()
plt.show()
```

L’objectif de préparation n’est pas de mémoriser une bibliothèque graphique entière, mais de pouvoir produire une visualisation simple et lisible rapidement.

---

# 6. Thème 4 — Valeurs manquantes et colonnes catégorielles

## Source

Le sujet annonce explicitement :

```text
gestion des valeurs manquantes
gestion des colonnes catégorielles
```

## Valeurs manquantes

### Identifier

```python
df.isna().sum()
```

### Supprimer

```python
df = df.dropna()
```

### Imputer

```python
df["age"] = df["age"].fillna(df["age"].median())
```

## Colonnes catégorielles

### Identifier

```python
df.select_dtypes(include=["object", "category"])
```

### Réflexe ML proposé

Selon le modèle choisi :

```python
pd.get_dummies(df, columns=["category"])
```

> Cette technique est un réflexe de préparation ; le support fourni annonce la gestion des colonnes catégorielles mais n’impose pas une méthode particulière.

---

# 7. Thème 5 — Base relationnelle avec Docker

## Source

Le support annonce la création d’une base de données relationnelle avec Docker et son administration via une interface de gestion.

Le cours ORM fourni utilise :

```text
PostgreSQL
pgAdmin
Docker Compose
```

Dans l’exercice ORM, le fichier `compose.yaml` démarre notamment :

```text
PostgreSQL
pgAdmin
```

## Réflexes Docker

```bash
docker ps
docker images
docker logs <container>
docker stop <container>
docker rm <container>
```

Avec Compose :

```bash
docker compose up -d
docker compose ps
docker compose logs
docker compose down
```

## À comprendre

```text
container
image
port
volume
environment
service
```

---

# 8. Thème 6 — Variables d’environnement

## Source

Le sujet mentionne l’utilisation de variables d’environnement :

```text
dans les fichiers Docker
et
dans les scripts Python
```

## Réflexe de révision

### `.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dst_db
DB_USER=user
DB_PASSWORD=password
```

### Python

```python
import os

db_host = os.getenv("DB_HOST")
```

### Docker Compose

```yaml
services:
  db:
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
```

## À retenir

```text
Code
≠
Configuration
≠
Secrets
```

---

# 9. Thème 7 — Modélisation relationnelle

## Source

Le support cite :

```text
schéma logique
clés primaires
clés étrangères
```

## Questions de révision

Pour chaque table :

```text
Quel est le grain ?
Quelle est la clé primaire ?
Quelles colonnes sont obligatoires ?
Existe-t-il une relation ?
Où se trouve la clé étrangère ?
```

## Modèle mental

```text
User
 │
 │ 1
 │
 └───────────────┐
                 │ N
              Address
```

---

# 10. Thème 8 — SQLAlchemy

# 10.1 Ce que le support ORM présente

## Source

Le cours ORM commence par expliquer que SQLAlchemy permet de se connecter et d’interagir avec plusieurs systèmes de bases de données.

Le support cite notamment :

```text
SQLite
PostgreSQL
MySQL & MariaDB
Oracle
Microsoft SQL Server
```

Il compare cette approche à une interaction plus directement liée à un connecteur spécifique.

---

# 10.2 `create_engine`

## Source

Le cours montre une connexion PostgreSQL via :

```python
from sqlalchemy import create_engine, text
```

avec une chaîne de connexion de type :

```text
postgresql+psycopg://user:password@host:port/database
```

## Réflexe

```python
engine = create_engine(DATABASE_URL)
```

---

# 11. Thème 8 — ORM : Object-Relational Mapping

## Source

Le cours introduit explicitement :

```text
Object-Relational Mapping
```

et explique que l’interaction avec la base peut être réalisée via des **classes Python** plutôt qu’en écrivant directement tout le SQL.

---

# 11.1 Base déclarative

## Source

Le support montre :

```python
from sqlalchemy.orm import declarative_base

Base = declarative_base()
```

---

# 11.2 Colonnes et types

## Source

Le cours introduit notamment :

```text
Column
Integer
String
```

Exemple proche de celui du support :

```python
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user = Column(String)
```

## À retenir

```text
classe Python
↔
table SQL
```

---

# 11.3 Création des tables

## Source

Le support utilise :

```python
Base.metadata.create_all(engine)
```

et présente également l’utilisation de :

```text
checkfirst
```

pour gérer le cas où la table existe déjà.

Il évoque aussi :

```python
Base.metadata.drop_all(...)
```

pour la suppression.

---

# 11.4 Session ORM

## Source

Le support introduit :

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
```

---

# 11.5 Insertion

## Source

Exemple présenté dans le cours :

```python
new_user = User(id=37, user="Nintri")

session.add(new_user)
session.commit()
```

Le support montre également que la clé primaire peut être attribuée automatiquement lorsque l’ID n’est pas fourni.

---

# 11.6 Lecture

## Source

Le cours utilise :

```python
users = session.query(User).all()
```

puis itère sur les résultats.

---

# 11.7 Filtrage

## Source

Le support présente notamment :

```python
session.query(User).filter_by(id=1).all()
```

Le message important du cours est qu’il faut connaître le principe du filtre sans nécessairement mémoriser l’ensemble de l’API SQLAlchemy.

---

# 11.8 Clé étrangère et relation

## Source

La section **Relations entre tables** présente :

```python
ForeignKey
relationship
```

Exemple fondé sur le support :

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
```

Puis le support crée d’abord un utilisateur, puis une adresse qui référence cet utilisateur.

## À retenir

```text
ForeignKey
=
contrainte relationnelle

relationship
=
navigation ORM
```

---

# 12. ORM — mini-cheatsheet

## Source + condensation

```python
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,
)

engine = create_engine(DATABASE_URL)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

user = User(name="Alice")
session.add(user)
session.commit()

users = session.query(User).all()
```

---

# 13. Thème 9 — Machine Learning avec scikit-learn

## Source

Le sujet annonce :

```text
entraînement d’un modèle de machine learning
avec scikit-learn
```

Le support ne fixe pas dans la page fournie un algorithme précis.

## Réflexe de révision

Pipeline minimal :

```text
X / y
↓
train_test_split
↓
fit
↓
predict
↓
metric
```

Exemple de squelette :

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
```

> Le choix du modèle et de la métrique dépendra du sujet réel.

---

# 14. Thème 10 — Sauvegarde avec joblib

## Source

Le sujet mentionne :

```text
évaluation
et
sauvegarde d’un modèle ML avec joblib
```

## Réflexe de révision

```python
import joblib

joblib.dump(model, "model.joblib")
```

Chargement :

```python
model = joblib.load("model.joblib")
```

---

# 15. Thème 11 — docker-compose pour collecte et ingestion

## Source

Le sujet annonce :

```text
mise en place d’un environnement de production
pour de la collecte et ingestion de données
via docker-compose
```

## À comprendre

```text
services
ports
environment
volumes
depends_on
```

## Squelette de révision

```yaml
services:
  db:
    image: postgres
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app

  app:
    build: .
    depends_on:
      - db
```

> Ce squelette est un exemple de préparation et non le fichier demandé explicitement par le sujet.

---

# 16. Thème 12 — Tests d’ingestion

## Source

Le support cite trois objectifs :

```text
gestion des erreurs
détection de doublons
conformité au schéma
```

## Réflexe de révision

### Test nominal

```text
donnée valide
→ ingestion réussie
```

### Erreur

```text
entrée invalide
→ erreur contrôlée
```

### Doublon

```text
même clé métier
→ doublon détecté
```

### Schéma

```text
colonne obligatoire absente
→ rejet ou erreur
```

## Réflexe pytest proposé

```python
def test_duplicate_is_detected():
    ...
```

> Le sujet fourni demande des tests robustes mais ne fixe pas dans cette page une implémentation unique.

---

# 17. Thème 13 — Impact écologique

## Source

Le support demande :

```text
estimation de l’impact écologique
d’un projet data
```

et indique qu’une recherche simple peut être réalisée.

## À préparer

Être capable de commenter brièvement :

```text
temps d’exécution
ressources utilisées
CPU
mémoire
stockage
durée de fonctionnement
```

## Important

Le support fourni ne donne pas de formule d’évaluation environnementale obligatoire.

Ne pas inventer une méthodologie officielle pendant l’examen si elle n’est pas demandée.

---

# 18. Livrables : checklist principale

## Source

Le support demande notamment :

- [ ] notebook d’exploration ;
- [ ] script Python d’extraction / transformation ;
- [ ] script de création de base via ORM ;
- [ ] script d’ingestion ;
- [ ] script d’entraînement ML ;
- [ ] fichier synthétique sur :
  - [ ] architecture ;
  - [ ] choix techniques ;
  - [ ] pistes d’amélioration.

## Réflexe de fin d’examen

```text
Chaque livrable existe-t-il ?
Chaque fichier s’ouvre-t-il ?
Le code principal est-il exécutable ?
Le ZIP contient-il tout ?
```

---

# 19. Les commandes à savoir sans hésiter

## Docker

```bash
docker ps
docker logs <container>
docker compose up -d
docker compose ps
docker compose logs
docker compose down
```

## Python

```bash
python script.py
```

## Environnement

```bash
python -m venv .venv
source .venv/bin/activate
```

Sous Windows :

```powershell
.venv\Scripts\activate
```

## Installation

```bash
pip install pandas matplotlib sqlalchemy scikit-learn joblib
```

> La liste exacte des dépendances peut varier selon le sujet et l’environnement fourni.

---

# 20. Les syntaxes Python à revoir en priorité

```text
pd.read_json
head
info
isna
fillna
dropna
drop_duplicates
groupby
sort_values

create_engine
declarative_base
Column
Integer
String
ForeignKey
relationship
create_all
sessionmaker
add
commit
query
filter_by

train_test_split
fit
predict

joblib.dump
joblib.load
```

---

# 21. Les erreurs classiques à éviter

## Réflexes de préparation

### Erreur 1

```text
Faire toute la logique dans le notebook.
```

À la fin, le sujet attend aussi des scripts.

---

### Erreur 2

```text
Coder l’ORM avant de comprendre les relations.
```

D’abord :

```text
grain
PK
FK
relations
```

puis :

```text
classes SQLAlchemy
```

---

### Erreur 3

```text
Passer trop de temps sur un modèle ML sophistiqué.
```

La page de préparation demande un modèle fonctionnel et une chaîne complète.

---

### Erreur 4

```text
Laisser Docker pour la fin.
```

Une erreur de port, de mot de passe ou de connexion peut consommer beaucoup de temps.

---

### Erreur 5

```text
Oublier la documentation.
```

Le fichier synthétique fait partie du rendu annoncé.

---

# 22. Auto-évaluation express

Répondre sans documentation.

## JSON / pandas

1. Comment charger un JSON avec pandas ?
2. Comment compter les valeurs manquantes ?
3. Comment détecter des doublons ?
4. Comment filtrer un DataFrame ?

## SQL / ORM

5. À quoi sert `create_engine()` ?
6. Que représente `Base` ?
7. À quoi sert `__tablename__` ?
8. Comment définir une clé primaire ?
9. À quoi sert `sessionmaker()` ?
10. Quelle différence entre `ForeignKey` et `relationship` ?
11. Comment insérer un objet ?
12. Comment récupérer tous les objets d’une table ?

## ML

13. Quel est le rôle de `train_test_split` ?
14. Quelle est la différence entre `fit()` et `predict()` ?
15. Comment sauvegarder un modèle avec `joblib` ?

## Docker

16. Comment lancer un Compose ?
17. Comment voir les logs ?
18. À quoi sert un volume ?
19. Pourquoi utiliser des variables d’environnement ?

## Qualité

20. Quels sont les trois types de contrôle explicitement annoncés pour l’ingestion ?

Réponse attendue pour la question 20 :

```text
gestion des erreurs
détection de doublons
conformité au schéma
```

---

# 23. Révision flash — 5 minutes

Avant de fermer cette fiche, être capable de réciter :

```text
1. JSON → Jupyter
2. pandas → nettoyage
3. Python → scripts réutilisables
4. PK / FK → schéma relationnel
5. SQLAlchemy → classes ORM
6. session → add / commit / query
7. scikit-learn → fit / predict
8. joblib → dump
9. Docker Compose → environnement
10. tests → erreur / doublon / schéma
11. documentation → architecture / choix / améliorations
12. archive → vérification finale
```

---

# 24. Contrainte de passage à ne pas oublier

## Source

Mereos impose notamment :

```text
caméra
microphone
localisation
pas de second écran
```

Les pauses sont possibles mais :

```text
le minuteur continue
```

Le candidat doit également :

```text
valider son identité
tester son micro
filmer son environnement
partager tout son écran
```

---

# 25. Priorités de révision

## Réflexe de préparation

### Priorité 1 — savoir reconstruire

```text
pandas ETL
SQLAlchemy ORM
Docker Compose
scikit-learn
```

### Priorité 2 — savoir diagnostiquer

```text
données manquantes
doublons
erreur de connexion
erreur de schéma
container en erreur
```

### Priorité 3 — savoir terminer

```text
documentation
tests
joblib
ZIP
upload
```

---

# 26. Résumé final

## Source

L’épreuve annoncée couvre une chaîne complète :

```text
exploration
→ transformation
→ base relationnelle
→ ORM
→ ingestion
→ ML
→ sauvegarde
→ conteneurisation
→ tests
→ synthèse
```

## Réflexe de préparation

Pour réussir la préparation, viser trois niveaux :

```text
JE COMPRENDS
    ↓
JE SAIS REFAIRE
    ↓
JE SAIS REFAIRE VITE
```

Le Bloc 2 doit être abordé comme un mini-projet **end-to-end** plutôt que comme une succession de questions indépendantes.

---

# 27. Document suivant

```text
02_RNCP_38919_BLOC_2_MEGA_CHEATSHEET.md
```

Objectif du prochain document :

> réduire cette fiche à l’essentiel opérationnel : commandes, snippets, syntaxes et patterns à retrouver en quelques secondes.
