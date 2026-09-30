# 11 — RNCP 38919 — Bloc 2
# Examen blanc 01 — Projet ETL & ML

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Type :** Examen blanc proposé à partir du périmètre du support DataScientest  
**Durée cible :** 4 heures  
**Niveau visé :** simulation complète du Bloc 2

**Sources de cadrage :**
- `Examen_Bloc_2_RNCP_Data_Engineer_Projet_ETL_ML.md`
- `Examen RNCP 38919 _ Bloc 2 - ORM.pdf`
- `Consignes surveillance évaluation.pdf`

> **Important**
>
> Ceci est un **sujet blanc créé pour l’entraînement**.
> Ce n’est pas un sujet officiel DataScientest et il ne prétend pas reproduire les questions réelles.
>
> Sa structure est construite pour couvrir les thèmes explicitement annoncés dans la ressource de préparation :
>
> ```text
> JSON / Jupyter
> Python structuré
> pandas / matplotlib
> valeurs manquantes
> colonnes catégorielles
> base relationnelle / Docker
> variables d’environnement
> PK / FK
> SQLAlchemy / ORM
> scikit-learn
> évaluation / joblib
> docker-compose
> tests d’ingestion
> impact écologique
> ```

---

# 1. Conditions de simulation

Pour que cet examen blanc soit utile, reproduire autant que possible les contraintes de l’épreuve :

```text
Durée : 4 h
Un seul écran
Chronomètre continu
Pas de corrigé ouvert
Pas de document 12 avant la fin
Rendu sous forme d’archive
```

Le support officiel précise que l’épreuve réelle dure 4 heures et est surveillée via Mereos.

---

# 2. Scénario métier — GreenDelivery

## Sujet blanc proposé

La société **GreenDelivery** opère un service de livraison urbaine en Île-de-France.

Elle collecte des événements de livraison sous forme de fichiers JSON.

Chaque événement contient notamment :

```text
identifiant de livraison
identifiant client
ville
type de véhicule
distance
niveau de trafic
météo
durée réelle
retard ou non
```

L’entreprise souhaite mettre en place un premier pipeline permettant de :

```text
1. explorer les données ;
2. les nettoyer ;
3. les stocker dans une base relationnelle ;
4. automatiser leur ingestion ;
5. entraîner un modèle capable de prédire un retard ;
6. tester la fiabilité du pipeline ;
7. documenter l’architecture et ses limites.
```

---

# 3. Donnée source

Vous disposez d’un fichier :

```text
deliveries.json
```

contenant des données similaires à celles placées en annexe de ce document.

Le dataset comporte volontairement :

```text
valeurs manquantes
catégories textuelles
variantes de casse / espaces
au moins un doublon
plusieurs clients
plusieurs villes
une target binaire
```

La target du sujet blanc est :

```text
late_delivery
```

avec :

```text
0 = livraison non en retard
1 = livraison en retard
```

---

# 4. Contraintes générales

Votre solution doit rester :

```text
simple
reproductible
documentée
testable
```

Le sujet blanc n’impose pas une architecture logicielle avancée.

Évitez les abstractions qui ne contribuent pas directement au rendu.

---

# 5. Partie A — Exploration des données

## Travail demandé

Créer :

```text
notebooks/01_exploration.ipynb
```

Le notebook doit permettre de comprendre le dataset.

Vous devez au minimum examiner :

```text
nombre de lignes
nombre de colonnes
noms de colonnes
types
valeurs manquantes
doublons
distribution de la target
variables catégorielles
variables numériques
```

---

# 6. Partie A.1 — Questions d’exploration

Répondre dans le notebook :

1. Quel est le grain du fichier source ?
2. Quelle colonne peut jouer le rôle de clé métier d’une livraison ?
3. Existe-t-il des doublons ?
4. Quelles colonnes contiennent des valeurs manquantes ?
5. Quelles colonnes sont catégorielles ?
6. La colonne `customer_city` nécessite-t-elle une normalisation ?
7. Quelle est la distribution de `late_delivery` ?
8. Quelles variables semblent potentiellement utiles pour prédire un retard ?

---

# 7. Partie A.2 — Visualisation

Créer au minimum :

```text
une visualisation de la target
```

et :

```text
une visualisation d’une variable numérique
```

avec :

```text
matplotlib
```

Les graphiques doivent avoir un titre lisible.

---

# 8. Partie B — Extraction et transformation

Créer :

```text
src/etl.py
```

Le script doit contenir une logique structurée et réutilisable.

Une organisation possible est :

```text
extract
validate
transform
save
```

Vous êtes libre de choisir les noms exacts.

---

# 9. Partie B.1 — Extraction

Le script doit :

```text
lire deliveries.json
retourner une structure exploitable avec pandas
échouer de manière explicite si le fichier n’existe pas
```

---

# 10. Partie B.2 — Validation minimale

Votre pipeline doit contrôler au minimum la présence de :

```text
delivery_id
customer_id
customer_city
vehicle_type
distance_km
traffic_level
weather
delivery_minutes
late_delivery
```

Si une colonne requise manque :

```text
l’ingestion ne doit pas continuer silencieusement
```

---

# 11. Partie B.3 — Nettoyage

Traiter les problèmes observés dans les données.

Votre transformation doit notamment prendre une décision explicite concernant :

```text
valeurs manquantes
doublons
casse / espaces de customer_city
colonnes catégorielles
types numériques
```

Documenter brièvement vos choix.

---

# 12. Partie B.4 — Dataset transformé

Produire un fichier :

```text
data/processed/deliveries_clean.csv
```

Le fichier doit être exploitable par les étapes suivantes.

---

# 13. Partie C — Modélisation relationnelle

Concevoir une base relationnelle contenant au minimum deux entités :

```text
Customer
Delivery
```

Relation attendue :

```text
Customer
   1
   │
   │
   N
Delivery
```

---

# 14. Partie C.1 — Schéma logique

Dans votre fichier synthétique, représenter le schéma logique.

Minimum attendu :

```text
customers
─────────
customer_id PK
customer_city

deliveries
──────────
delivery_id PK
customer_id FK
vehicle_type
distance_km
traffic_level
weather
delivery_minutes
late_delivery
```

Vous pouvez améliorer ce modèle si votre choix est justifié.

---

# 15. Partie C.2 — Questions de modélisation

Expliquer brièvement :

1. Pourquoi `customer_id` est-il la PK de `customers` ?
2. Pourquoi `delivery_id` est-il la PK de `deliveries` ?
3. Où doit se trouver la FK ?
4. Quelle cardinalité existe entre les deux tables ?
5. Quels champs peuvent être nullable après nettoyage ?

---

# 16. Partie D — Base relationnelle sous Docker

## Hypothèse d’entraînement du sujet blanc

Pour ce sujet blanc, utilisez :

```text
MySQL ou MariaDB
+
phpMyAdmin
```

via Docker.

> Ce choix est propre au **sujet blanc** afin de suivre la mention `phpMyAdmin`
> du support principal. Il ne préjuge pas de la stack de l’examen réel.

---

# 17. Partie D.1 — Docker Compose

Créer :

```text
docker-compose.yml
```

contenant au minimum :

```text
un service de base relationnelle
un service phpMyAdmin
un volume persistant
des variables d’environnement
```

---

# 18. Partie D.2 — Variables d’environnement

Créer :

```text
.env
```

et ne pas dupliquer inutilement les credentials dans le code Python.

Votre configuration doit permettre d’exprimer au minimum :

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

---

# 19. Partie D.3 — Persistance

La base doit utiliser :

```text
un volume Docker
```

afin que les données ne disparaissent pas lors d’un simple redémarrage des containers.

---

# 20. Partie E — SQLAlchemy / ORM

Créer :

```text
src/models.py
```

et :

```text
src/database.py
```

ou une organisation équivalente.

Le code doit utiliser :

```text
SQLAlchemy
ORM
```

---

# 21. Partie E.1 — Modèles ORM

Définir au minimum :

```text
Customer
Delivery
```

avec :

```text
__tablename__
colonnes
PK
FK
relationship
```

---

# 22. Partie E.2 — Création des tables

Créer :

```text
src/create_database.py
```

ou un script équivalent permettant de créer les tables à partir des modèles ORM.

Le script doit pouvoir être exécuté sans passer par le notebook.

---

# 23. Partie F — Ingestion

Créer :

```text
src/ingest.py
```

Le script doit ingérer les données transformées dans la base.

Ordre logique recommandé :

```text
customers
↓
deliveries
```

afin de respecter la relation de clé étrangère.

---

# 24. Partie F.1 — Fiabilité

L’ingestion doit éviter de produire silencieusement :

```text
clients dupliqués
livraisons dupliquées
clés étrangères invalides
```

Votre choix peut être :

```text
rejet
déduplication
contrôle préalable
```

mais il doit être cohérent et documenté.

---

# 25. Partie F.2 — Vérification

Après ingestion, fournir une preuve simple que :

```text
les tables existent
les données sont présentes
les relations sont cohérentes
```

Cette preuve peut apparaître dans :

```text
le terminal
le notebook
phpMyAdmin
ou le fichier synthétique
```

---

# 26. Partie G — Machine Learning

Créer :

```text
src/train_model.py
```

Objectif :

```text
prédire late_delivery
```

---

# 27. Partie G.1 — Préparation des features

Définir :

```text
X
y
```

avec :

```text
y = late_delivery
```

Justifier les colonnes supprimées des features.

Exemple de question à se poser :

```text
delivery_id apporte-t-il une information prédictive utile ?
```

---

# 28. Partie G.2 — Catégories et valeurs manquantes

Avant l’entraînement :

```text
gérer les colonnes catégorielles
gérer les valeurs manquantes restantes
```

La méthode est libre tant qu’elle est cohérente et reproductible.

---

# 29. Partie G.3 — Split

Séparer les données en :

```text
train
test
```

Le jeu de test ne doit pas servir à entraîner le modèle.

---

# 30. Partie G.4 — Modèle

Entraîner un modèle de classification avec :

```text
scikit-learn
```

Le choix de l’algorithme est libre.

Critère principal :

```text
modèle fonctionnel
et choix explicable
```

---

# 31. Partie G.5 — Évaluation

Calculer au moins :

```text
une métrique de classification
```

et interpréter le résultat en quelques phrases.

Attention :

```text
le dataset fourni dans ce sujet blanc est volontairement petit
```

Vous devez donc signaler que la performance mesurée est peu robuste.

---

# 32. Partie G.6 — Sauvegarde

Sauvegarder le modèle avec :

```text
joblib
```

dans :

```text
models/model.joblib
```

ou un chemin équivalent clairement documenté.

---

# 33. Partie H — Tests

Créer un ou plusieurs fichiers sous :

```text
tests/
```

Les tests doivent couvrir les trois axes annoncés dans le support de préparation :

```text
gestion des erreurs
détection de doublons
conformité au schéma
```

---

# 34. Partie H.1 — Tests minimums

Créer au minimum des tests équivalents à :

```text
dataset valide
colonne obligatoire absente
delivery_id dupliqué
erreur d’entrée contrôlée
```

---

# 35. Partie H.2 — Exécution

Votre rendu doit permettre de lancer les tests simplement.

Exemple :

```bash
pytest -v
```

---

# 36. Partie I — Impact écologique

Le support officiel annonce une estimation de l’impact écologique / consommation énergétique.

Pour ce sujet blanc :

1. identifier les principaux postes de consommation de votre solution ;
2. proposer au moins trois leviers de réduction ;
3. expliquer les limites de votre estimation.

Vous pouvez vous appuyer sur :

```text
durée d’exécution
CPU
RAM
stockage
containers actifs
fréquence d’exécution
volume de données
```

Aucune formule unique n’est imposée dans ce sujet blanc.

---

# 37. Partie J — Documentation

Créer :

```text
ARCHITECTURE.md
```

ou :

```text
README.md
```

Le document doit présenter au minimum :

```text
contexte
architecture
pipeline ETL
modèle relationnel
Docker / Compose
ORM
ingestion
ML
tests
impact écologique
choix techniques
limites
pistes d’amélioration
```

---

# 38. Architecture ASCII demandée

Inclure un schéma similaire dans l’esprit à :

```text
deliveries.json
      │
      ▼
Jupyter / pandas
      │
      ▼
ETL Python
      │
      ▼
deliveries_clean.csv
      │
      ├───────────────┐
      │               │
      ▼               ▼
SQLAlchemy ORM    scikit-learn
      │               │
      ▼               ▼
DB Docker        model.joblib
      │
      ▼
Tests / contrôle
```

Vous pouvez l’adapter à votre architecture réelle.

---

# 39. Livrables attendus pour ce sujet blanc

Votre archive doit contenir au minimum :

```text
notebooks/
  01_exploration.ipynb

src/
  etl.py
  database.py
  models.py
  create_database.py
  ingest.py
  train_model.py

tests/
  ...

data/
  raw/
  processed/

models/
  model.joblib

docker-compose.yml
.env.example
requirements.txt
README.md ou ARCHITECTURE.md
```

Le fichier `.env` réel peut être exclu de l’archive si les credentials sont considérés comme secrets, à condition qu’un `.env.example` documente les variables nécessaires.

---

# 40. Arborescence indicative

```text
green_delivery/
│
├── data/
│   ├── raw/
│   │   └── deliveries.json
│   └── processed/
│       └── deliveries_clean.csv
│
├── notebooks/
│   └── 01_exploration.ipynb
│
├── src/
│   ├── etl.py
│   ├── database.py
│   ├── models.py
│   ├── create_database.py
│   ├── ingest.py
│   └── train_model.py
│
├── tests/
│   └── ...
│
├── models/
│   └── model.joblib
│
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── ARCHITECTURE.md
```

Cette arborescence est indicative.

---

# 41. Critères d’auto-évaluation

Le sujet blanc est réussi si vous pouvez répondre oui à l’ensemble des questions suivantes :

```text
[ ] ai-je exploré les données ?
[ ] ai-je identifié nulls et doublons ?
[ ] ai-je produit un ETL rejouable ?
[ ] ai-je créé un schéma relationnel cohérent ?
[ ] ai-je utilisé PK / FK ?
[ ] ai-je créé les tables via ORM ?
[ ] ai-je lancé la base via Docker ?
[ ] ai-je utilisé des variables d’environnement ?
[ ] ai-je ingéré les données ?
[ ] ai-je entraîné un modèle scikit-learn ?
[ ] ai-je évalué le modèle ?
[ ] ai-je sauvegardé avec joblib ?
[ ] ai-je testé erreurs / doublons / schéma ?
[ ] ai-je traité l’impact écologique ?
[ ] ai-je documenté architecture et limites ?
[ ] ai-je créé une archive complète avant 4 h ?
```

---

# 42. Planning conseillé de simulation

> Planning proposé, non officiel.

```text
00:00–00:15
Lecture / cadrage

00:15–00:45
Notebook / exploration

00:45–01:20
ETL

01:20–02:00
Docker + DB + ORM

02:00–02:30
Ingestion

02:30–03:00
ML

03:00–03:25
Intégration / Compose

03:25–03:40
Tests

03:40–03:55
Documentation

03:55–04:00
Archive / vérification
```

---

# 43. Règles de simulation

Pour rendre le test réellement utile :

```text
ne pas ouvrir le corrigé
ne pas interrompre le chrono
ne pas passer 45 min sur un seul bug
ne pas remplacer un livrable manquant par une explication
```

À 03:55 :

```text
STOP CODING
```

---

# 44. Questions de soutenance personnelle

À la fin de la simulation, être capable de répondre oralement à :

1. Pourquoi avez-vous choisi ce schéma relationnel ?
2. Quelle est la différence entre PK et FK ?
3. Quel est le rôle de l’ORM ?
4. Quel est le rôle du volume Docker ?
5. Pourquoi utiliser des variables d’environnement ?
6. Comment avez-vous géré les doublons ?
7. Comment avez-vous géré les valeurs manquantes ?
8. Quel modèle ML avez-vous choisi et pourquoi ?
9. Quelle métrique avez-vous utilisée ?
10. Pourquoi le score obtenu doit-il être interprété avec prudence ?
11. Quels tests protègent l’ingestion ?
12. Quelles sont les principales limites de votre solution ?

---

# 45. Post-mortem obligatoire

Une fois le chrono arrêté, noter :

```text
temps réel exploration
temps réel ETL
temps réel ORM
temps réel Docker
temps réel ingestion
temps réel ML
temps réel tests
temps réel documentation
```

Puis répondre :

```text
Quel bloc m’a fait perdre le plus de temps ?
Quelle syntaxe ai-je dû rechercher ?
Quel bug ai-je mal diagnostiqué ?
Ai-je livré avant 4 h ?
Qu’est-ce que je dois automatiser avant le prochain blanc ?
```

---

# 46. Annexe — `deliveries.json`

Pour rendre ce document autonome, le dataset synthétique du sujet blanc est fourni ci-dessous.

Copiez ce contenu dans :

```text
data/raw/deliveries.json
```

```json
[
  {
    "delivery_id": 1001,
    "customer_id": 501,
    "customer_city": "Paris",
    "vehicle_type": "bike",
    "distance_km": 4.2,
    "traffic_level": "high",
    "weather": "rain",
    "delivery_minutes": 38,
    "late_delivery": 1
  },
  {
    "delivery_id": 1002,
    "customer_id": 502,
    "customer_city": "Poissy",
    "vehicle_type": "car",
    "distance_km": 18.4,
    "traffic_level": "medium",
    "weather": "clear",
    "delivery_minutes": 42,
    "late_delivery": 0
  },
  {
    "delivery_id": 1003,
    "customer_id": 503,
    "customer_city": "PARIS",
    "vehicle_type": "bike",
    "distance_km": 3.1,
    "traffic_level": "low",
    "weather": "clear",
    "delivery_minutes": 19,
    "late_delivery": 0
  },
  {
    "delivery_id": 1004,
    "customer_id": 501,
    "customer_city": " Paris ",
    "vehicle_type": "scooter",
    "distance_km": 7.8,
    "traffic_level": "high",
    "weather": "rain",
    "delivery_minutes": 47,
    "late_delivery": 1
  },
  {
    "delivery_id": 1005,
    "customer_id": 504,
    "customer_city": "Versailles",
    "vehicle_type": "car",
    "distance_km": 15.0,
    "traffic_level": "medium",
    "weather": "clear",
    "delivery_minutes": 34,
    "late_delivery": 0
  },
  {
    "delivery_id": 1006,
    "customer_id": 505,
    "customer_city": "Poissy",
    "vehicle_type": "bike",
    "distance_km": null,
    "traffic_level": "medium",
    "weather": "wind",
    "delivery_minutes": 31,
    "late_delivery": 0
  },
  {
    "delivery_id": 1007,
    "customer_id": 506,
    "customer_city": "Nanterre",
    "vehicle_type": "scooter",
    "distance_km": 9.7,
    "traffic_level": null,
    "weather": "clear",
    "delivery_minutes": 44,
    "late_delivery": 1
  },
  {
    "delivery_id": 1008,
    "customer_id": 507,
    "customer_city": "Paris",
    "vehicle_type": "car",
    "distance_km": 12.4,
    "traffic_level": "high",
    "weather": "rain",
    "delivery_minutes": 58,
    "late_delivery": 1
  },
  {
    "delivery_id": 1009,
    "customer_id": 508,
    "customer_city": "Boulogne-Billancourt",
    "vehicle_type": "bike",
    "distance_km": 5.5,
    "traffic_level": "low",
    "weather": "clear",
    "delivery_minutes": 24,
    "late_delivery": 0
  },
  {
    "delivery_id": 1010,
    "customer_id": 509,
    "customer_city": "Nanterre",
    "vehicle_type": "car",
    "distance_km": 11.1,
    "traffic_level": "medium",
    "weather": "wind",
    "delivery_minutes": 37,
    "late_delivery": 0
  },
  {
    "delivery_id": 1011,
    "customer_id": 510,
    "customer_city": "Paris",
    "vehicle_type": "scooter",
    "distance_km": 6.2,
    "traffic_level": "high",
    "weather": "clear",
    "delivery_minutes": 41,
    "late_delivery": 1
  },
  {
    "delivery_id": 1012,
    "customer_id": 511,
    "customer_city": "Versailles",
    "vehicle_type": "bike",
    "distance_km": 8.0,
    "traffic_level": "medium",
    "weather": "rain",
    "delivery_minutes": 35,
    "late_delivery": 0
  },
  {
    "delivery_id": 1013,
    "customer_id": 512,
    "customer_city": "Poissy",
    "vehicle_type": "car",
    "distance_km": 20.2,
    "traffic_level": "high",
    "weather": "rain",
    "delivery_minutes": 64,
    "late_delivery": 1
  },
  {
    "delivery_id": 1014,
    "customer_id": 513,
    "customer_city": "Nanterre",
    "vehicle_type": "scooter",
    "distance_km": 10.4,
    "traffic_level": "low",
    "weather": "clear",
    "delivery_minutes": 29,
    "late_delivery": 0
  },
  {
    "delivery_id": 1015,
    "customer_id": 514,
    "customer_city": "Boulogne-Billancourt",
    "vehicle_type": "bike",
    "distance_km": 4.7,
    "traffic_level": "medium",
    "weather": null,
    "delivery_minutes": 32,
    "late_delivery": 0
  },
  {
    "delivery_id": 1016,
    "customer_id": 515,
    "customer_city": "Paris",
    "vehicle_type": "car",
    "distance_km": 13.8,
    "traffic_level": "high",
    "weather": "wind",
    "delivery_minutes": 52,
    "late_delivery": 1
  },
  {
    "delivery_id": 1017,
    "customer_id": 516,
    "customer_city": "Poissy",
    "vehicle_type": "scooter",
    "distance_km": 7.0,
    "traffic_level": "low",
    "weather": "clear",
    "delivery_minutes": 26,
    "late_delivery": 0
  },
  {
    "delivery_id": 1018,
    "customer_id": 517,
    "customer_city": "Versailles",
    "vehicle_type": "car",
    "distance_km": 16.3,
    "traffic_level": "medium",
    "weather": "rain",
    "delivery_minutes": 49,
    "late_delivery": 1
  },
  {
    "delivery_id": 1019,
    "customer_id": 518,
    "customer_city": "Paris",
    "vehicle_type": "bike",
    "distance_km": 5.0,
    "traffic_level": "high",
    "weather": "rain",
    "delivery_minutes": 39,
    "late_delivery": 1
  },
  {
    "delivery_id": 1020,
    "customer_id": 519,
    "customer_city": "Nanterre",
    "vehicle_type": "scooter",
    "distance_km": 8.9,
    "traffic_level": "medium",
    "weather": "clear",
    "delivery_minutes": 33,
    "late_delivery": 0
  },
  {
    "delivery_id": 1020,
    "customer_id": 519,
    "customer_city": "Nanterre",
    "vehicle_type": "scooter",
    "distance_km": 8.9,
    "traffic_level": "medium",
    "weather": "clear",
    "delivery_minutes": 33,
    "late_delivery": 0
  },
  {
    "delivery_id": 1021,
    "customer_id": 520,
    "customer_city": "Paris",
    "vehicle_type": "bike",
    "distance_km": 2.9,
    "traffic_level": "low",
    "weather": "clear",
    "delivery_minutes": 17,
    "late_delivery": 0
  },
  {
    "delivery_id": 1022,
    "customer_id": 521,
    "customer_city": "Poissy",
    "vehicle_type": "car",
    "distance_km": 19.3,
    "traffic_level": "high",
    "weather": "rain",
    "delivery_minutes": 61,
    "late_delivery": 1
  },
  {
    "delivery_id": 1023,
    "customer_id": 522,
    "customer_city": "Boulogne-Billancourt",
    "vehicle_type": "scooter",
    "distance_km": 6.6,
    "traffic_level": "medium",
    "weather": "wind",
    "delivery_minutes": 36,
    "late_delivery": 0
  }
]
```

---

# 47. Particularités volontairement introduites dans le dataset

Sans donner la solution détaillée, le dataset contient volontairement plusieurs situations à repérer :

```text
valeurs manquantes
doublon
variantes de casse / espaces
variables catégorielles
plusieurs observations par ville
plusieurs observations de la target
```

Votre travail consiste à les détecter et à décider comment les gérer.

---

# 48. Fin du sujet

Lorsque les 4 heures sont écoulées :

```text
STOP
```

Ne consultez le corrigé qu’après avoir :

```text
créé votre archive
noté votre temps
rédigé votre post-mortem
```

---

# 49. Document suivant

```text
12_RNCP_38919_BLOC_2_CORRIGE_EXAMEN_BLANC_01.md
```

Le prochain document contiendra le corrigé détaillé de ce sujet blanc :

```text
analyse attendue
ETL
modèle relationnel
Docker
ORM
ingestion
ML
tests
documentation
points de contrôle
et erreurs fréquentes
```
