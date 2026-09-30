# 00 — RNCP 38919 — Bloc 2  
# Analyse complète et stratégie de préparation

**Certification :** RNCP 38919 — Data Engineer  
**Bloc :** Bloc 2  
**Module DataScientest :** Sprint 19 — Préparation RNCP 38919  
**Épreuve principale :** Examen Bloc 2 — Projet ETL & ML  
**Durée officielle de l’examen :** 4 heures  
**Ressource complémentaire :** ORM — 120 min  
**Sources utilisées :**
- `Examen RNCP 38919 _ Bloc 2 - Projet ETL & ML.pdf`
- `Examen RNCP 38919 _ Bloc 2 - ORM.pdf`
- `Consignes surveillance évaluation.pdf`

---

## 1. Objet du document

Ce document sert de **document maître de préparation** pour l’épreuve RNCP 38919 — Bloc 2.

Il poursuit quatre objectifs :

1. extraire précisément les attentes exprimées dans les supports DataScientest ;
2. cartographier les compétences techniques à maîtriser ;
3. organiser une stratégie de préparation progressive ;
4. définir une méthode d’exécution adaptée à une épreuve de **4 heures sous surveillance**.

> Les sections intitulées **Attendu officiel** reprennent uniquement le périmètre visible dans les supports fournis.  
> Les sections intitulées **Stratégie proposée** correspondent à une organisation de préparation construite à partir de ces attentes.

---

# 2. Position du Bloc 2 dans le Sprint 19

Le module visible dans DataScientest est organisé ainsi :

```text
Sprint 19 — Préparation RNCP 38919
│
└── Examen RNCP 38919 — Bloc 2
    │
    ├── 1. Examen — Bloc 2      240 min
    │
    └── 2. ORM                  120 min
    │
    └── Total pédagogique ≈ 6 h
```

Il faut distinguer :

```text
240 min
=
durée de l'épreuve principale

120 min
=
ressource de préparation ORM
```

La durée affichée de l’ensemble du module n’est donc pas la durée effective de l’examen.

---

# 3. Format officiel de l’épreuve

## 3.1 Durée

Le support de surveillance indique :

```text
4 heures
EN DIRECT avec Learn + Mereos
```

L’examen est donc :

- minuté ;
- réalisé en ligne ;
- surveillé ;
- associé à la plateforme Learn ;
- associé au système de surveillance Mereos.

---

# 4. Contraintes de surveillance Mereos

## 4.1 Avant l’examen

Le candidat doit :

```text
installer l’extension Mereos
sur Google Chrome
```

Le déroulement annoncé est :

```text
Plateforme Learn
      ↓
MES EXAMS
      ↓
COMMENCER L’EXAMEN
      ↓
TAKE WITH MEREOS
      ↓
Configuration de la session
```

---

## 4.2 Vérification du système

Mereos vérifie les paramètres du système.

La session nécessite l’accès à :

- la caméra ;
- le microphone ;
- la localisation / GPS.

Le support précise également :

```text
LE SECOND ÉCRAN N’EST PAS AUTORISÉ
```

Cette contrainte est importante pour la préparation :

> toute la stratégie doit être pensée pour fonctionner efficacement sur un seul écran.

---

## 4.3 Pauses

Les pauses sont autorisées.

Cependant :

```text
le minuteur ne s’arrête pas
```

Il faut donc préparer avant le démarrage :

- eau ;
- nourriture si nécessaire ;
- pièce d’identité ;
- environnement de travail ;
- matériel ;
- session informatique ;
- outils de développement.

---

## 4.4 Validation de l’environnement

Avant de commencer, le candidat doit notamment :

1. prendre sa photo ;
2. prendre la photo de sa pièce d’identité ;
3. tester son microphone ;
4. filmer son environnement ;
5. partager tout son écran ;
6. accepter les règles ;
7. confirmer l’exactitude des informations.

Le partage de l’écran est enregistré.

---

# 5. Nature technique de l’épreuve

Le Bloc 2 correspond à un **mini-projet Data Engineering / ETL / ML complet**.

Il ne s’agit pas uniquement :

```text
de faire du Machine Learning
```

mais de construire une chaîne cohérente :

```text
Données
  ↓
Exploration
  ↓
Transformation
  ↓
Stockage
  ↓
ORM
  ↓
Ingestion
  ↓
Machine Learning
  ↓
Évaluation
  ↓
Sauvegarde du modèle
  ↓
Industrialisation
  ↓
Tests
```

---

# 6. Les 13 sujets abordés officiellement

Le support du Bloc 2 annonce treize thèmes.

---

## 6.1 Exploration JSON avec Jupyter

### Attendu officiel

```text
Exploration de données au format JSON
à l’aide de notebooks Jupyter
```

### Compétences à maîtriser

- ouvrir un fichier JSON ;
- inspecter sa structure ;
- comprendre le grain du dataset ;
- identifier les colonnes utiles ;
- repérer les types ;
- repérer les valeurs manquantes ;
- préparer une première exploration.

### Preuve attendue

Un notebook d’exploration.

---

## 6.2 Scripts Python structurés et réutilisables

### Attendu officiel

```text
développement de scripts Python
structurés et réutilisables
```

### Compétences à maîtriser

Savoir passer de :

```python
# code exploratoire dans un notebook
```

à :

```python
def extract(...):
    ...

def transform(...):
    ...

def load(...):
    ...
```

Le code doit être organisé de manière suffisamment claire pour être :

- relu ;
- exécuté ;
- réutilisé ;
- testé.

---

## 6.3 Pandas et Matplotlib

### Attendu officiel

Le support mentionne :

```text
pandas
matplotlib
```

### Compétences à maîtriser

Avec `pandas` :

- `read_json`
- `DataFrame`
- sélection de colonnes
- filtres
- tris
- agrégations
- `groupby`
- nettoyage
- gestion des types
- valeurs manquantes

Avec `matplotlib` :

- visualisation simple ;
- lecture rapide d’une distribution ;
- graphique exploitable dans un notebook.

---

# 7. Nettoyage des données

## 7.1 Valeurs manquantes

Le support mentionne explicitement la gestion des valeurs manquantes.

Révisions indispensables :

```python
df.isna()
df.isna().sum()
df.dropna()
df.fillna(...)
```

Il faut également être capable de justifier le choix :

```text
supprimer
ou
imputer
```

---

## 7.2 Colonnes catégorielles

Le support annonce également :

```text
gestion des colonnes catégorielles
```

Il faut donc savoir identifier :

```text
numérique
catégoriel
booléen
date
texte
```

et préparer les données pour leur exploitation ultérieure.

---

# 8. Base de données relationnelle et Docker

## 8.1 Attendu officiel

Le sujet demande la création d’une base de données relationnelle avec Docker et son administration via une interface dédiée.

Le candidat doit être à l’aise avec :

```text
Docker
base SQL
conteneurs
variables d’environnement
persistance
```

---

## 8.2 Docker minimal à maîtriser

Commandes et notions fondamentales :

```bash
docker ps
docker images
docker run
docker stop
docker rm
docker logs
```

et surtout :

```bash
docker compose up -d
docker compose down
```

---

# 9. Variables d’environnement

## 9.1 Attendu officiel

Les variables d’environnement sont mentionnées à deux endroits :

```text
fichiers Docker
scripts Python
```

Il faut comprendre la séparation :

```text
Code
≠
Configuration
≠
Secrets
```

Exemple :

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=rncp
DB_USER=rncp_user
DB_PASSWORD=...
```

Puis côté Python :

```python
import os

host = os.getenv("DB_HOST")
```

---

# 10. Modélisation relationnelle

## 10.1 Attendu officiel

Le support cite :

```text
schéma logique
clés primaires
clés étrangères
```

Le candidat doit pouvoir passer rapidement de données brutes vers :

```text
Entités
   ↓
Tables
   ↓
Primary Keys
   ↓
Foreign Keys
   ↓
Relations
```

---

## 10.2 Questions à se poser

Pour chaque table :

```text
Quel est le grain ?
Quelle est la clé primaire ?
Quelles colonnes sont obligatoires ?
Existe-t-il une relation avec une autre table ?
Quelle colonne porte la clé étrangère ?
```

---

# 11. SQLAlchemy et ORM

La présence d’un module ORM de deux heures montre que ce point mérite une préparation spécifique.

---

## 11.1 Chaîne conceptuelle

```text
Python
  ↓
Classe ORM
  ↓
SQLAlchemy
  ↓
Table SQL
  ↓
Base de données
```

---

## 11.2 Concepts à maîtriser

Le niveau attendu doit permettre de comprendre et reproduire rapidement :

```text
engine
declarative base
model
table
column
primary key
foreign key
relationship
session
insert
query
commit
```

---

## 11.3 Modèle minimal de référence

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
```

---

## 11.4 Création des tables

```python
Base.metadata.create_all(engine)
```

---

## 11.5 Session

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
```

---

## 11.6 Insertion

```python
user = User(name="Alice")

session.add(user)
session.commit()
```

---

## 11.7 Lecture

```python
users = session.query(User).all()
```

---

## 11.8 Relations

Il faut maîtriser la logique :

```text
Parent
  1
  │
  │
  N
Enfant
```

avec notamment :

```python
ForeignKey(...)
relationship(...)
```

---

# 12. Machine Learning

## 12.1 Attendu officiel

Le support cite explicitement :

```text
scikit-learn
```

Il faut entraîner un modèle de Machine Learning.

---

## 12.2 Pipeline minimal à savoir reconstruire

```text
DataFrame
   ↓
Features X
Target y
   ↓
train_test_split
   ↓
model.fit()
   ↓
model.predict()
   ↓
metric
```

---

## 12.3 Objectif

L’objectif n’est probablement pas de construire un système ML complexe.

La priorité est de démontrer la chaîne :

```text
préparer
entraîner
évaluer
sauvegarder
```

---

# 13. Sauvegarde du modèle avec joblib

## 13.1 Attendu officiel

Le support cite :

```text
joblib
```

La compétence minimale est :

```python
import joblib

joblib.dump(model, "model.joblib")
```

et éventuellement :

```python
model = joblib.load("model.joblib")
```

---

# 14. Docker Compose et environnement de production

## 14.1 Attendu officiel

Le support demande :

```text
mise en place d’un environnement de production
pour la collecte et l’ingestion de données
via docker-compose
```

---

## 14.2 Architecture minimale

```text
docker-compose
│
├── database
│
├── administration DB
│
└── application / ingestion
```

Selon le sujet réel, certaines briques pourront être plus ou moins importantes.

---

# 15. Tests de l’ingestion

## 15.1 Attendu officiel

Les tests doivent vérifier notamment :

```text
gestion des erreurs
détection des doublons
conformité au schéma
```

---

## 15.2 Trois familles prioritaires

### Erreurs

```text
fichier manquant
JSON invalide
connexion DB impossible
donnée invalide
```

### Doublons

```text
même identifiant
même clé métier
réingestion du même enregistrement
```

### Schéma

```text
colonnes attendues
types attendus
colonnes obligatoires
```

---

# 16. Impact écologique

## 16.1 Attendu officiel

Le sujet mentionne :

```text
estimation de l’impact écologique
du projet data
```

et précise qu’une recherche simple peut être suffisante.

L’objectif est donc de produire une estimation argumentée, pas nécessairement une étude environnementale approfondie.

---

# 17. Livrables attendus

Le support indique que le rendu doit contenir :

```text
1. un notebook d’exploration de données

2. un script Python reprenant
   les étapes d’extraction et transformation

3. un script de création de base de données
   via ORM

4. un script d’ingestion dans la base

5. un script d’entraînement du modèle ML

6. un fichier synthétique expliquant :
   - l’architecture
   - les choix techniques
   - les pistes d’amélioration
```

Cette liste doit devenir la checklist centrale de l’examen.

---

# 18. Structure de projet recommandée

## Stratégie proposée

```text
rncp38919_bloc2/
│
├── notebooks/
│   └── 01_exploration.ipynb
│
├── src/
│   ├── transform.py
│   ├── database.py
│   ├── ingest.py
│   └── train_model.py
│
├── models/
│   └── model.joblib
│
├── tests/
│   └── test_ingestion.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docker-compose.yml
├── .env
├── requirements.txt
├── README.md
└── architecture.md
```

Le sujet officiel peut imposer une organisation différente.

Cette structure sert donc de **réflexe mental**, pas de contrainte absolue.

---

# 19. Architecture cible de travail

```text
             JSON
               │
               ▼
      ┌─────────────────┐
      │ Jupyter Notebook│
      │   Exploration   │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │     pandas      │
      │ Transformation  │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │ SQLAlchemy ORM  │
      │ Models / Schema │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │  SQL Database   │
      │     Docker      │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │    Ingestion    │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │ scikit-learn    │
      │ Train / Evaluate│
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │     joblib      │
      │ Persist model   │
      └─────────────────┘
```

En parallèle :

```text
Docker Compose
Tests
Documentation
Impact écologique
```

---

# 20. Matrice de compétences

| Domaine | Attente | Preuve possible |
|---|---|---|
| Jupyter | Explorer le JSON | Notebook |
| Python | Code structuré | Scripts |
| Pandas | Transformer | DataFrame propre |
| Matplotlib | Visualiser | Graphique |
| Data Quality | Gérer nulls/catégories | Transformation |
| Docker | Déployer les services | Containers actifs |
| SQL | Modéliser | Tables + PK/FK |
| SQLAlchemy | ORM | Classes Python |
| Ingestion | Charger en DB | Script fonctionnel |
| ML | Entraîner | Modèle scikit-learn |
| Évaluation | Mesurer | Métrique |
| Joblib | Sauvegarder | `.joblib` |
| Compose | Orchestrer | `docker-compose.yml` |
| Tests | Fiabiliser | Tests d’ingestion |
| Green IT | Estimer | Section synthétique |

---

# 21. Risques principaux pendant l’épreuve

## 21.1 Surinvestir l’exploration

Risque :

```text
30 à 60 minutes perdues
dans le notebook
```

Le notebook doit permettre de comprendre le dataset.

Il ne doit pas absorber toute l’épreuve.

---

## 21.2 Déboguer Docker trop longtemps

Le risque le plus coûteux est :

```text
15 min
  ↓
30 min
  ↓
60 min
```

sur un problème de :

```text
port
variable
volume
mot de passe
container name
network
```

---

## 21.3 Surcomplexifier l’ORM

Éviter :

```text
architecture DDD
repositories avancés
patterns complexes
abstractions inutiles
```

Le besoin est d’abord :

```text
Classes
Tables
Relations
Session
Ingestion
```

---

## 21.4 Chercher un modèle ML trop sophistiqué

Un modèle simple et fonctionnel vaut mieux qu’un pipeline avancé inachevé.

---

## 21.5 Documentation laissée pour les dernières minutes

Le fichier synthétique est un livrable attendu.

Il doit être alimenté progressivement.

---

# 22. Stratégie d’exécution proposée — 4 heures

La répartition suivante n’est pas une consigne officielle.

Elle constitue une stratégie de passage.

---

## 00:00 → 00:15 — Lecture et cadrage

```text
Lire intégralement le sujet
Identifier les livrables
Identifier les fichiers fournis
Identifier la target ML
Identifier les tables attendues
Créer l’arborescence
```

Objectif :

```text
ne pas coder avant de comprendre
```

---

## 00:15 → 00:45 — Exploration

```text
charger JSON
inspecter structure
décrire dataset
valeurs manquantes
types
target
visualisation minimale
```

Livrable :

```text
01_exploration.ipynb
```

---

## 00:45 → 01:20 — Transformation Python

Créer :

```text
extract
transform
clean
```

Puis vérifier que le script peut être exécuté indépendamment du notebook.

---

## 01:20 → 02:00 — Base + ORM

```text
docker / database
models SQLAlchemy
PK/FK
create_all
session
```

---

## 02:00 → 02:30 — Ingestion

```text
load transformed data
verify row counts
verify duplicates
verify schema
```

---

## 02:30 → 03:00 — Machine Learning

```text
X / y
split
fit
predict
metric
joblib.dump
```

---

## 03:00 → 03:25 — Docker Compose / industrialisation

Vérifier :

```text
services
environment
volumes
depends_on
restart
```

---

## 03:25 → 03:40 — Tests

Priorité :

```text
happy path
invalid data
duplicate
schema error
```

---

## 03:40 → 03:55 — Documentation

Finaliser :

```text
architecture
choix techniques
limites
améliorations
impact écologique
```

---

## 03:55 → 04:00 — Packaging final

```text
STOP CODING
```

Puis :

```text
vérifier les fichiers
supprimer les fichiers inutiles
tester rapidement
créer l’archive
vérifier l’archive
uploader
```

---

# 23. Règle de gestion du temps

Toutes les 30 minutes :

```text
TIMER
  ↓
Où en suis-je ?
  ↓
Le livrable courant fonctionne-t-il ?
  ↓
Dois-je poursuivre ?
  ↓
Ou passer au suivant ?
```

Principe :

> Un livrable simple terminé vaut mieux qu’un livrable sophistiqué incomplet.

---

# 24. Plan de préparation recommandé

## Phase 1 — Révision ciblée

Créer :

```text
01_BLOC_2_FICHE_REVISION.md
02_BLOC_2_MEGA_CHEATSHEET.md
```

---

## Phase 2 — Exercices atomiques

Faire séparément :

```text
JSON → pandas
pandas → clean
SQLAlchemy → PostgreSQL
ORM relations
ingestion
ML
joblib
docker-compose
pytest
```

Objectif :

```text
chaque brique doit être familière
avant de les combiner
```

---

## Phase 3 — Mini-projet

Créer un petit dataset et construire :

```text
JSON
→ ETL
→ PostgreSQL
→ ML
→ tests
```

sans limite de temps.

---

## Phase 4 — Simulation partielle

Réaliser le même exercice en :

```text
2 heures
```

afin de travailler la vitesse.

---

## Phase 5 — Examen blanc intégral

Conditions :

```text
4 heures
1 écran
chronomètre
aucune interruption
environnement propre
archive finale obligatoire
```

---

# 25. Documents à produire ensuite

Ordre recommandé :

```text
01_RNCP_38919_BLOC_2_FICHE_REVISION.md

02_RNCP_38919_BLOC_2_MEGA_CHEATSHEET.md

03_RNCP_38919_BLOC_2_ETL_PYTHON_GUIDE.md

04_RNCP_38919_BLOC_2_SQLALCHEMY_ORM_GUIDE.md

05_RNCP_38919_BLOC_2_DOCKER_COMPOSE_GUIDE.md

06_RNCP_38919_BLOC_2_MACHINE_LEARNING_GUIDE.md

07_RNCP_38919_BLOC_2_TESTING_STRATEGY.md

08_RNCP_38919_BLOC_2_TEMPLATE_PROJECT.md

09_RNCP_38919_BLOC_2_STRATEGIE_EXAMEN_4H.md

10_RNCP_38919_BLOC_2_CHECKLIST_JOUR_J.md

11_RNCP_38919_BLOC_2_EXAMEN_BLANC_01.md

12_RNCP_38919_BLOC_2_CORRIGE_EXAMEN_BLANC_01.md
```

---

# 26. Checklist de maîtrise avant examen

## Python / Data

- [ ] Je sais ouvrir un JSON.
- [ ] Je sais inspecter rapidement un DataFrame.
- [ ] Je sais traiter les valeurs manquantes.
- [ ] Je sais gérer des colonnes catégorielles.
- [ ] Je sais produire une visualisation simple.
- [ ] Je sais transformer un notebook en script.

## SQL / ORM

- [ ] Je sais modéliser une PK.
- [ ] Je sais modéliser une FK.
- [ ] Je sais créer une relation 1-N.
- [ ] Je sais définir une classe SQLAlchemy.
- [ ] Je sais créer les tables.
- [ ] Je sais ouvrir une session.
- [ ] Je sais insérer des données.
- [ ] Je sais interroger des données.

## Docker

- [ ] Je sais lancer un container.
- [ ] Je sais utiliser Docker Compose.
- [ ] Je sais déclarer des variables.
- [ ] Je sais déclarer un volume.
- [ ] Je sais lire les logs.
- [ ] Je sais nettoyer un environnement.

## Machine Learning

- [ ] Je sais construire X et y.
- [ ] Je sais faire un train/test split.
- [ ] Je sais entraîner un modèle.
- [ ] Je sais calculer une métrique.
- [ ] Je sais sauvegarder avec joblib.

## Qualité

- [ ] Je sais tester une ingestion valide.
- [ ] Je sais tester une donnée invalide.
- [ ] Je sais détecter un doublon.
- [ ] Je sais vérifier un schéma.

## Rendu

- [ ] Notebook.
- [ ] Script ETL.
- [ ] Script ORM.
- [ ] Script ingestion.
- [ ] Script ML.
- [ ] Documentation.
- [ ] Archive vérifiée.

---

# 27. Modèle mental à retenir

```text
         COMPRENDRE
             │
             ▼
           JSON
             │
             ▼
          JUPYTER
             │
             ▼
           PANDAS
             │
             ▼
        TRANSFORMER
             │
             ▼
        SQLALCHEMY
             │
             ▼
        BASE DE DONNÉES
             │
             ▼
          INGÉRER
             │
             ▼
             ML
             │
             ▼
          JOBLIB
             │
             ▼
     DOCKER / COMPOSE
             │
             ▼
           TESTS
             │
             ▼
      DOCUMENTER
             │
             ▼
        LIVRER .ZIP
```

---

# 28. Conclusion

Le Bloc 2 n’évalue pas une technologie isolée.

Il vérifie la capacité à faire fonctionner une chaîne complète :

```text
Données
  +
Python
  +
ETL
  +
SQL / ORM
  +
Docker
  +
Machine Learning
  +
Tests
  +
Documentation
```

sous une contrainte déterminante :

```text
4 HEURES
```

La meilleure préparation n’est donc pas seulement :

```text
connaître les concepts
```

mais :

```text
être capable de les assembler rapidement
```

jusqu’à produire :

```text
un système simple
+
fonctionnel
+
testable
+
documenté
+
livrable
```

Le fil directeur de la préparation doit rester :

> **Comprendre vite → construire simplement → valider systématiquement → livrer complètement.**
