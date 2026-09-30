# 10 — RNCP 38919 — Bloc 2
# Checklist Jour J

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 2 — Projet ETL & ML  
**Durée officielle :** 4 heures  
**Surveillance :** Learn + Mereos

**Sources utilisées :**
- `Consignes surveillance évaluation.pdf`
- `Examen RNCP 38919 _ Bloc 2 - Projet ETL & ML.pdf`
- `Examen RNCP 38919 _ Bloc 2 - ORM.pdf`

> **Important**
>
> Les sections **Officiel** reprennent les éléments présents dans les supports fournis.
> Les sections **Organisation proposée** servent de checklist pratique pour le jour J.
> Elles ne remplacent jamais les consignes affichées dans Learn ou Mereos.

---

# 1. Format officiel à garder en tête

## Officiel

```text
Durée : 4 heures
Mode : EN DIRECT
Plateformes : Learn + Mereos
Navigateur : Chrome
```

La session Mereos demande notamment :

```text
caméra
microphone
GPS / localisation
partage de tout l’écran
```

Le support précise :

```text
LE SECOND ÉCRAN N’EST PAS AUTORISÉ
```

et :

```text
les pauses sont autorisées
mais le minuteur ne s’arrête pas
```

---

# 2. Veille de l’examen

## Organisation proposée

### Matériel

```text
[ ] ordinateur chargé
[ ] chargeur prêt
[ ] caméra fonctionnelle
[ ] microphone fonctionnel
[ ] connexion Internet stable
[ ] second écran débranché / désactivé
```

### Navigateur / surveillance

```text
[ ] Google Chrome installé
[ ] extension Mereos installée
[ ] accès Learn vérifié
[ ] accès à MES EXAMS vérifié
```

### Identité

```text
[ ] pièce d’identité prête
```

### Environnement de travail

```text
[ ] bureau dégagé
[ ] environnement présentable pour la vidéo Mereos
[ ] eau prête
[ ] tout ce qui est utile est préparé avant le départ du chrono
```

---

# 3. Vérification technique avant l’examen

## Organisation proposée

### Python

```text
[ ] Python fonctionne
[ ] environnement virtuel possible
[ ] pip fonctionne
```

Commandes de test :

```bash
python --version
pip --version
```

### Docker

```text
[ ] Docker démarre
[ ] docker ps fonctionne
[ ] docker compose fonctionne
```

Commandes :

```bash
docker ps
docker compose version
```

### Jupyter

```text
[ ] notebook exécutable
```

### Éditeur / terminal

```text
[ ] IDE ouvert
[ ] terminal ouvert
[ ] aucun ancien projet parasite
```

---

# 4. Réflexes techniques à avoir sous la main mentalement

## Bloc ETL

```text
pd.read_json
head
info
isna
duplicated
dropna
fillna
drop_duplicates
groupby
to_csv
```

## Bloc ORM

```text
create_engine
declarative_base
Column
Integer
String
primary_key
ForeignKey
relationship
create_all
sessionmaker
add
commit
query
filter_by
```

## Bloc Docker

```text
docker ps
docker logs
docker compose up -d
docker compose ps
docker compose logs
docker compose down
```

## Bloc ML

```text
X / y
train_test_split
fit
predict
metric
joblib.dump
```

## Bloc Tests

```text
schéma
doublons
erreurs
happy path
```

---

# 5. 30 minutes avant le démarrage

## Organisation proposée

```text
[ ] fermer les applications inutiles
[ ] désactiver les notifications
[ ] fermer les onglets non utiles
[ ] vérifier l’espace disque
[ ] vérifier batterie / secteur
[ ] vérifier réseau
[ ] préparer ID
[ ] préparer eau
[ ] vérifier Docker
[ ] vérifier Chrome
[ ] vérifier Mereos
```

Ne pas démarrer l’épreuve en étant encore en train de :

```text
installer Docker
chercher son mot de passe
configurer le micro
nettoyer son bureau
```

---

# 6. Démarrage Mereos

## Officiel

Le flux indiqué dans le support est :

```text
Learn
  ↓
MES EXAMS
  ↓
COMMENCER L’EXAMEN
  ↓
TAKE WITH MEREOS
  ↓
configuration de la session
```

Puis Mereos demande notamment :

```text
photo
photo de l’ID
test micro
vidéo de l’environnement
partage complet de l’écran
acceptation des règles
```

---

# 7. Check de démarrage immédiat

## Organisation proposée

Dès que le sujet est visible :

```text
[ ] lire tout le sujet
[ ] ne pas coder immédiatement
[ ] repérer les livrables
[ ] repérer les fichiers fournis
[ ] repérer le dataset
[ ] repérer la target ML
[ ] repérer la base demandée
[ ] repérer les relations PK / FK
[ ] repérer les contraintes Docker
```

---

# 8. Checklist des livrables

## Source

Le support principal demande notamment :

```text
[ ] notebook d’exploration
[ ] script extraction / transformation
[ ] script création de base via ORM
[ ] script ingestion
[ ] script entraînement ML
[ ] fichier synthétique
```

Le fichier synthétique doit notamment couvrir :

```text
architecture
choix techniques
pistes d’amélioration
```

---

# 9. Checklist exploration

## Organisation proposée

```text
[ ] JSON chargé
[ ] shape vérifiée
[ ] colonnes vérifiées
[ ] types vérifiés
[ ] nulls vérifiés
[ ] doublons vérifiés
[ ] catégories identifiées
[ ] target identifiée
[ ] décisions de nettoyage notées
```

---

# 10. Checklist ETL

```text
[ ] extract()
[ ] validate_schema()
[ ] transform()
[ ] output généré
[ ] nulls traités
[ ] doublons contrôlés
[ ] catégories normalisées
```

---

# 11. Checklist Base / ORM

```text
[ ] moteur de connexion créé
[ ] Base définie
[ ] classes ORM créées
[ ] __tablename__ présent
[ ] PK définies
[ ] FK définies
[ ] relationship définies si besoin
[ ] create_all exécuté
[ ] Session fonctionnelle
```

---

# 12. Checklist Ingestion

```text
[ ] DataFrame propre
[ ] objets ORM construits
[ ] session.add(...)
[ ] session.commit()
[ ] nombre de lignes vérifié
[ ] doublons vérifiés
[ ] relations vérifiées
```

---

# 13. Checklist Docker / Compose

```text
[ ] services définis
[ ] ports corrects
[ ] variables env correctes
[ ] volume défini
[ ] DB démarrée
[ ] outil admin accessible si demandé
[ ] application peut joindre la DB
```

Commandes :

```bash
docker compose up -d
docker compose ps
docker compose logs
```

---

# 14. Checklist Machine Learning

```text
[ ] target définie
[ ] X défini
[ ] catégories gérées
[ ] nulls gérés
[ ] train/test split
[ ] model.fit()
[ ] model.predict()
[ ] métrique calculée
[ ] modèle sauvegardé avec joblib
```

---

# 15. Checklist Tests

## Source

Les tests doivent couvrir notamment :

```text
gestion des erreurs
détection de doublons
conformité au schéma
```

## Organisation proposée

```text
[ ] happy path
[ ] colonne manquante
[ ] doublon
[ ] erreur critique
```

---

# 16. Checkpoint à 1 heure

## Organisation proposée

À environ 1 h :

```text
[ ] sujet compris
[ ] notebook avancé
[ ] transformation définie
```

Question :

```text
Suis-je déjà en train de surinvestir l’exploration ?
```

Si oui :

```text
passer au script
```

---

# 17. Checkpoint à 2 heures

À mi-parcours :

```text
[ ] ETL fonctionnel
[ ] base démarrée
[ ] ORM créé
```

Si ce n’est pas le cas :

```text
SIMPLIFIER
```

et éviter tout ajout secondaire.

---

# 18. Checkpoint à 3 heures

```text
[ ] ingestion fonctionnelle
[ ] modèle ML entraîné
[ ] score obtenu
[ ] joblib produit
```

Si non :

```text
aucun tuning
aucun refactor avancé
aucune visualisation supplémentaire
```

---

# 19. Checkpoint à 3 h 30

```text
[ ] tests prioritaires écrits
[ ] documentation commencée
[ ] tous les livrables existent
```

À partir de ce moment :

```text
ne plus ouvrir de nouveau chantier
```

---

# 20. Checkpoint à 3 h 55

```text
STOP CODING
```

Faire uniquement :

```text
[ ] sauvegarder
[ ] vérifier fichiers
[ ] vérifier archive
[ ] uploader
```

---

# 21. Checklist de debug rapide

## ETL

```text
fichier ?
JSON valide ?
colonnes ?
types ?
nulls ?
doublons ?
```

## ORM

```text
DB UP ?
URL correcte ?
driver installé ?
Base ?
PK ?
create_all ?
Session ?
commit ?
```

## Docker

```text
docker compose ps
docker compose logs
ports
env
host
password
volume
```

## ML

```text
target ?
NaN ?
strings ?
mêmes colonnes ?
fit ?
```

---

# 22. Règle anti-blocage

## Organisation proposée

Si un bug consomme déjà beaucoup de temps :

```text
LIRE
↓
DIAGNOSTIQUER
↓
SIMPLIFIER
↓
CONTOURNER
↓
DOCUMENTER
↓
CONTINUER
```

Ne pas perdre une heure sur une seule brique.

---

# 23. Ce qu’il ne faut pas faire

```text
[ ] ne pas surcomplexifier l’ORM
[ ] ne pas lancer de tuning ML long
[ ] ne pas refaire toute l’architecture
[ ] ne pas ajouter des technologies non demandées
[ ] ne pas attendre la dernière minute pour documenter
[ ] ne pas attendre 03:59 pour créer le ZIP
```

---

# 24. Fichier synthétique — checklist

```text
[ ] architecture
[ ] données sources
[ ] ETL
[ ] modèle relationnel
[ ] Docker / Compose
[ ] ML
[ ] tests
[ ] choix techniques
[ ] limites
[ ] pistes d’amélioration
[ ] impact écologique
```

---

# 25. Impact écologique

## Source

Le support principal demande une estimation de l’impact écologique du projet data.

## Organisation proposée

Vérifier que le fichier synthétique contient au moins une réflexion courte sur :

```text
temps d’exécution
ressources utilisées
CPU / mémoire
stockage
services / containers actifs
```

Ne pas inventer de méthode officielle si le sujet n’en fournit pas.

---

# 26. Avant création de l’archive

```text
[ ] pas de fichier temporaire inutile
[ ] pas de cache inutile
[ ] noms de fichiers clairs
[ ] notebook présent
[ ] scripts présents
[ ] tests présents
[ ] doc présente
[ ] modèle présent si demandé
[ ] configuration présente
```

---

# 27. Vérification de l’archive

```text
[ ] archive créée
[ ] archive ouvrable
[ ] contenu vérifié
[ ] pas de dossier racine vide inattendu
[ ] tous les livrables présents
```

---

# 28. Upload final

```text
[ ] bon fichier sélectionné
[ ] upload terminé
[ ] confirmation visible
```

Ne pas considérer le rendu terminé tant que l’upload n’est pas effectivement finalisé.

---

# 29. Checklist ultra-courte à mémoriser

```text
READ
↓
EXPLORE
↓
ETL
↓
ORM
↓
INGEST
↓
ML
↓
TEST
↓
DOC
↓
ZIP
↓
UPLOAD
```

---

# 30. Les 10 vérifications finales

```text
1. Sujet lu entièrement ?
2. Tous les livrables existent ?
3. Notebook lisible ?
4. ETL exécutable ?
5. DB / ORM fonctionnels ?
6. Ingestion vérifiée ?
7. ML entraîné et évalué ?
8. Tests présents ?
9. Documentation présente ?
10. ZIP uploadé ?
```

---

# 31. Phrase de rappel

> **Le jour J : couvrir, vérifier, livrer.**

---

# 32. Document suivant

```text
11_RNCP_38919_BLOC_2_EXAMEN_BLANC_01.md
```

Objectif :

> passer maintenant de la préparation à une simulation complète :
> un sujet réaliste, chronométré sur 4 heures, couvrant JSON, ETL, ORM, Docker,
> ingestion, Machine Learning, tests, documentation et rendu final.
