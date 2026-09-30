# 09 — RNCP 38919 — Bloc 2
# Stratégie d’examen 4 h

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 2 — Projet ETL & ML  
**Durée officielle :** 4 heures  
**Surveillance :** Learn + Mereos

**Sources de cadrage :**
- `Examen RNCP 38919 _ Bloc 2 - Projet ETL & ML.pdf`
- `Consignes surveillance évaluation.pdf`
- `Examen RNCP 38919 _ Bloc 2 - ORM.pdf`

> **Important**
>
> Les supports fournis fixent le périmètre technique, les livrables principaux et la durée de l’épreuve.
> Ils **ne donnent pas** un découpage minute par minute.
>
> Le planning ci-dessous est donc une **stratégie de passage proposée**, construite pour sécuriser le maximum de livrables dans les 4 heures.

---

# 1. Contraintes officielles à intégrer dans la stratégie

## Source

L’épreuve dure :

```text
4 heures
```

et se déroule :

```text
EN DIRECT avec Learn + Mereos
```

Le support de surveillance indique notamment :

```text
Chrome requis
caméra
microphone
localisation / GPS
second écran interdit
partage complet de l’écran
```

Les pauses sont autorisées mais :

```text
le minuteur ne s’arrête pas
```

Conséquence stratégique :

> le jour J, le temps doit être considéré comme une ressource non récupérable.

---

# 2. Ce que l’examen demande de couvrir

## Source

Le support Bloc 2 annonce notamment :

```text
JSON / Jupyter
Python structuré
pandas / matplotlib
valeurs manquantes
colonnes catégorielles
base relationnelle
Docker
variables d’environnement
PK / FK
SQLAlchemy / ORM
scikit-learn
joblib
docker-compose
tests d’ingestion
impact écologique
```

Le rendu doit notamment contenir :

```text
notebook d’exploration
script extraction / transformation
script création DB via ORM
script ingestion
script entraînement ML
fichier synthétique
```

La stratégie doit donc viser :

```text
couverture complète
avant optimisation locale
```

---

# 3. Principe directeur

## Stratégie proposée

```text
TERMINER
>
PERFECTIONNER
```

Autrement dit :

```text
un livrable simple mais fonctionnel
>
un livrable sophistiqué inachevé
```

---

# 4. Vue d’ensemble des 4 heures

## Stratégie proposée

```text
00:00 – 00:15  Lecture + cadrage
00:15 – 00:45  Exploration Jupyter
00:45 – 01:20  ETL Python / pandas
01:20 – 02:00  Base + SQLAlchemy ORM
02:00 – 02:30  Ingestion
02:30 – 03:00  Machine Learning
03:00 – 03:25  Docker Compose / intégration
03:25 – 03:40  Tests
03:40 – 03:55  Documentation
03:55 – 04:00  ZIP + vérification + upload
```

Total :

```text
240 minutes
```

---

# 5. Phase 0 — Avant de cliquer sur « commencer »

## Source

Le support Mereos demande de préparer :

```text
pièce d’identité
caméra
microphone
environnement
partage écran
```

et précise que les pauses ne stoppent pas le chrono.

## Stratégie proposée

Avant de démarrer :

```text
[ ] eau prête
[ ] pièce d’identité prête
[ ] Chrome ouvert
[ ] Mereos installé
[ ] Docker opérationnel
[ ] terminal prêt
[ ] IDE / éditeur prêt
[ ] espace disque disponible
[ ] aucun second écran actif
[ ] environnement de travail propre
```

---

# 6. 00:00 – 00:15 — Lecture et cadrage

## Objectif

Ne pas coder immédiatement.

Faire :

```text
1. lire tout le sujet
2. lister les livrables
3. identifier les fichiers fournis
4. identifier le dataset
5. identifier la target ML
6. identifier le moteur DB
7. identifier les tables / relations
8. identifier les contraintes Docker
```

Créer immédiatement une checklist :

```text
[ ] notebook
[ ] ETL
[ ] ORM
[ ] ingestion
[ ] ML
[ ] tests
[ ] documentation
[ ] archive finale
```

---

# 7. Décision GO / NO-GO à 00:15

À 15 minutes :

```text
GO
→ périmètre compris

NO-GO
→ continuer à coder serait dangereux
```

Questions à pouvoir répondre :

```text
Quelle est la target ?
Quelles sont les entités ?
Quelle est la PK ?
Quelle est la FK ?
Quelle stack DB ?
Quels fichiers rendre ?
```

---

# 8. 00:15 – 00:45 — Exploration Jupyter

## Objectif

Comprendre suffisamment le dataset pour prendre les décisions suivantes.

Séquence :

```text
load
↓
head
↓
shape
↓
columns
↓
types
↓
nulls
↓
duplicates
↓
categories
↓
target
```

Commandes réflexes :

```python
df.head()
df.shape
df.columns
df.info()
df.isna().sum()
df.duplicated().sum()
```

---

# 9. Stop condition de la phase exploration

À 00:45 :

```text
STOP EXPLORATION
```

même si toutes les analyses possibles ne sont pas faites.

Il faut déjà savoir :

```text
- quelles colonnes garder
- quelles colonnes nettoyer
- quelle target utiliser
- quelle PK candidate existe
- quelles catégories nécessitent traitement
```

---

# 10. 00:45 – 01:20 — ETL Python

## Objectif

Passer du notebook au code rejouable.

Construire :

```text
extract()
validate_schema()
transform()
save_processed()
```

Minimum viable :

```python
def extract(...):
    ...

def transform(...):
    ...

def save_processed(...):
    ...
```

---

# 11. Checkpoint ETL à 01:20

Le script doit idéalement permettre :

```text
RAW JSON
→ dataset transformé
```

Checklist :

```text
[ ] script exécutable
[ ] colonnes attendues présentes
[ ] nulls principaux gérés
[ ] doublons contrôlés
[ ] catégories normalisées
[ ] output généré
```

---

# 12. 01:20 – 02:00 — Base + ORM

## Objectif

Construire la couche relationnelle.

Ordre :

```text
1. définir Base
2. définir classes
3. définir PK
4. définir FK
5. définir relationship
6. create_all
7. créer Session
8. tester connexion
```

Le support ORM travaille avec :

```text
create_engine
declarative_base
Column
Integer
String
primary_key
ForeignKey
relationship
sessionmaker
```

---

# 13. Stop condition ORM

À 02:00, il faut préférer :

```text
2 tables simples fonctionnelles
```

à :

```text
un modèle sophistiqué non exécutable
```

Minimum :

```text
engine OK
Base OK
table(s) créées
Session OK
```

---

# 14. 02:00 – 02:30 — Ingestion

## Objectif

Faire entrer les données transformées dans la base.

Pattern :

```text
DataFrame
→ objets ORM
→ session.add
→ session.commit
```

Vérifier :

```text
count
PK
FK
doublons
```

---

# 15. Checkpoint ingestion à 02:30

Checklist :

```text
[ ] données présentes
[ ] nombre de lignes cohérent
[ ] aucune duplication inattendue
[ ] relations correctes
[ ] erreurs critiques traitées
```

---

# 16. 02:30 – 03:00 — Machine Learning

## Objectif

Construire un pipeline ML simple.

Séquence :

```text
X / y
↓
catégories
↓
split
↓
fit
↓
predict
↓
metric
↓
joblib
```

À ce stade :

```text
simple
>
complexe
```

---

# 17. Stop condition ML

À 03:00 :

```text
[ ] modèle entraîné
[ ] prédictions produites
[ ] métrique calculée
[ ] model.joblib sauvegardé
```

Ne pas lancer une optimisation longue.

---

# 18. 03:00 – 03:25 — Docker Compose / intégration

## Objectif

S’assurer que l’environnement demandé est cohérent.

Vérifier :

```text
docker compose up -d
docker compose ps
docker compose logs
```

Puis :

```text
ports
env vars
volumes
connexion app → DB
```

---

# 19. Point de vigilance sur la stack

## Source

Les supports ne sont pas homogènes :

```text
support principal
→ phpMyAdmin

support ORM
→ PostgreSQL + pgAdmin
```

Stratégie :

> utiliser uniquement la stack explicitement demandée par le sujet reçu le jour J.

---

# 20. 03:25 – 03:40 — Tests

## Source

Le support annonce :

```text
gestion des erreurs
détection des doublons
conformité au schéma
```

## Stratégie proposée

Écrire au minimum :

```text
1. test nominal
2. test colonne manquante
3. test doublon
4. test erreur critique
```

---

# 21. Priorité tests

Si le temps devient critique :

```text
P0
schéma
doublon
erreur

P1
happy path

P2
cas supplémentaires
```

---

# 22. 03:40 – 03:55 — Documentation

## Source

Le rendu demande un fichier synthétique expliquant notamment :

```text
architecture
choix techniques
pistes d’amélioration
```

## Stratégie proposée

Structure minimale :

```text
1. architecture
2. pipeline ETL
3. modèle relationnel
4. ML
5. tests
6. choix techniques
7. limites
8. pistes d’amélioration
9. impact écologique
```

---

# 23. 03:55 – 04:00 — STOP CODING

À 03:55 :

```text
STOP CODING
```

Même si :

```text
une amélioration semble facile
```

Faire uniquement :

```text
1. vérifier fichiers
2. vérifier archive
3. vérifier noms
4. uploader
```

---

# 24. Checklist finale 5 minutes

```text
[ ] notebook présent
[ ] ETL présent
[ ] ORM présent
[ ] ingestion présente
[ ] ML présent
[ ] joblib présent si demandé
[ ] tests présents
[ ] documentation présente
[ ] archive créée
[ ] archive ouvrable
[ ] upload lancé
```

---

# 25. Règle des checkpoints

## Stratégie proposée

Toutes les 30 minutes :

```text
STOP 30 secondes
```

Questions :

```text
Où suis-je ?
Le livrable courant fonctionne-t-il ?
Suis-je en retard ?
Dois-je simplifier ?
```

---

# 26. Règle anti-tunnel

Ne jamais rester plus de :

```text
≈ 15 minutes
```

sur un bug sans réévaluer.

Si blocage :

```text
1. lire erreur
2. logs
3. simplifier
4. contourner
5. documenter limite
6. continuer
```

---

# 27. Décision de simplification

Exemples :

```text
ML trop complexe
→ modèle plus simple

ORM trop complexe
→ réduire relations

Docker instable
→ revenir au minimum viable demandé

Tests trop nombreux
→ garder 3–4 tests prioritaires
```

---

# 28. Bug budget

## Stratégie proposée

Budget maximum conseillé par bug :

```text
10–15 min
```

Puis décision :

```text
FIX
ou
WORKAROUND
ou
DOCUMENT
```

---

# 29. Ordre des priorités de livrables

```text
P0 — critiques
─────────────
notebook
ETL
ORM
ingestion
ML

P1 — sécurisation
────────────────
tests
docker-compose
documentation

P2 — amélioration
────────────────
visualisations supplémentaires
refactoring
optimisation
```

---

# 30. Si tu prends 20 minutes de retard

Scénario :

```text
heure prévue : 02:00
réalité       : 02:20
```

Action :

```text
supprimer sophistication
pas les livrables
```

Exemple :

```text
pas de tuning ML
pas de refactor avancé
tests minimum
documentation concise
```

---

# 31. Si tu prends 40 minutes de retard

Action immédiate :

```text
passer en mode MVP
```

MVP :

```text
ETL fonctionnel
DB fonctionnelle
ingestion fonctionnelle
ML simple
3 tests
doc concise
```

---

# 32. Si Docker bloque

Ordre de diagnostic :

```text
docker compose ps
↓
docker compose logs SERVICE
↓
ports
↓
env
↓
host
↓
credentials
↓
volume
```

Ne pas modifier 5 fichiers simultanément.

---

# 33. Si SQLAlchemy bloque

Checklist :

```text
DB up ?
URL correcte ?
driver installé ?
engine OK ?
Base définie ?
PK définie ?
create_all appelé ?
Session correcte ?
commit ?
```

---

# 34. Si pandas bloque

Checklist :

```text
fichier existe ?
JSON valide ?
colonnes présentes ?
types ?
nulls ?
doublons ?
```

---

# 35. Si ML bloque

Checklist :

```text
target existe ?
X sans target ?
NaN ?
strings non encodées ?
train/test cohérents ?
modèle adapté ?
```

---

# 36. Si pytest bloque

Checklist :

```text
imports ?
path ?
test_*.py ?
fonction test_* ?
données de test correctes ?
```

---

# 37. Règle du « chemin critique »

## Stratégie proposée

Toujours protéger :

```text
DATA
 ↓
ETL
 ↓
DB
 ↓
ML
 ↓
RENDU
```

Tout ce qui ne renforce pas ce chemin critique est secondaire.

---

# 38. Matrice temps / valeur

| Tâche | Valeur | Risque temps |
|---|---:|---:|
| Comprendre sujet | Très haute | Faible |
| ETL | Très haute | Moyen |
| ORM | Très haute | Moyen |
| Ingestion | Très haute | Moyen |
| ML simple | Haute | Faible |
| Tests minimum | Haute | Faible |
| Docker debug profond | Moyen | Très élevé |
| Tuning ML | Faible à moyen | Très élevé |
| Refactor avancé | Faible | Élevé |
| Visualisation avancée | Faible | Moyen |

---

# 39. Stratégie documentaire

Ne pas attendre 03:40 pour commencer totalement la documentation.

Pendant l’épreuve, noter progressivement :

```text
architecture
choix
limites
```

dans un fichier brouillon.

Puis finaliser à la fin.

---

# 40. Réflexe après chaque phase

Après chaque bloc :

```text
SAVE
```

et si pertinent :

```text
RUN
```

Objectif :

```text
ne jamais avoir 90 minutes
de code non testé
```

---

# 41. Réflexe « une preuve par phase »

```text
Exploration
→ notebook s’exécute

ETL
→ fichier output existe

ORM
→ table existe

Ingestion
→ lignes en DB

ML
→ score + model.joblib

Tests
→ pytest vert
```

---

# 42. Réflexe mono-écran

## Source

Le second écran est interdit.

## Stratégie proposée

Organisation pratique :

```text
moitié écran
→ sujet / documentation

moitié écran
→ IDE / terminal
```

Éviter :

```text
10 fenêtres ouvertes
```

---

# 43. Réflexe terminal

Garder disponibles :

```text
terminal 1
→ Docker / logs

terminal 2
→ Python / pytest
```

si l’environnement mono-écran reste lisible.

---

# 44. Pauses

## Source

Les pauses sont autorisées mais le chrono continue.

## Stratégie proposée

Éviter une pause longue.

Si nécessaire :

```text
2–3 minutes
```

à un checkpoint naturel, par exemple après :

```text
ETL
ou
ingestion
```

---

# 45. Ne pas changer de stack en cours d’épreuve

À éviter :

```text
PostgreSQL
→ problème
→ passer à MySQL
```

sauf si le sujet l’autorise et que le changement est clairement plus sûr.

Un changement de stack coûte :

```text
temps
+
risque
+
debug
```

---

# 46. Ne pas surdocumenter

Le fichier synthétique doit être :

```text
clair
court
factuel
```

pas :

```text
un mémoire de 30 pages
```

---

# 47. Ne pas sous-documenter

À l’inverse, ne pas rendre uniquement du code.

Le support demande explicitement un fichier synthétique.

---

# 48. Stratégie de nommage

Utiliser des noms simples :

```text
01_exploration.ipynb
etl.py
models.py
ingest.py
train_model.py
test_ingestion.py
ARCHITECTURE.md
```

Objectif :

```text
lisibilité immédiate
```

---

# 49. Stratégie de sauvegarde

Pendant l’épreuve :

```text
enregistrer souvent
```

et vérifier que le fichier est réellement sur disque.

---

# 50. Stratégie ZIP

Avant archive :

```text
supprimer
- cache
- fichiers temporaires
- artefacts inutiles
```

Conserver :

```text
code
notebook
config attendue
tests
documentation
artefacts demandés
```

---

# 51. Vérifier l’archive

Ne jamais supposer :

```text
ZIP créé
=
ZIP correct
```

Faire :

```text
ouvrir archive
vérifier fichiers
```

---

# 52. Simulation recommandée

Avant le vrai examen :

```text
4 heures
1 écran
aucune aide externe non prévue
chronomètre
dataset inconnu
archive finale obligatoire
```

Le but est de tester :

```text
la vitesse
pas seulement les connaissances
```

---

# 53. KPI personnel de simulation

À mesurer :

```text
temps lecture
temps ETL
temps ORM
temps ingestion
temps ML
temps tests
temps documentation
temps debug
temps finalisation
```

---

# 54. Critères de réussite d’un examen blanc

```text
[ ] rendu complet
[ ] aucun bloc majeur absent
[ ] code principal exécutable
[ ] DB fonctionnelle
[ ] ML fonctionnel
[ ] tests ciblés
[ ] archive livrée avant 4 h
```

---

# 55. Post-mortem après simulation

Après chaque examen blanc :

```text
Qu’est-ce qui m’a fait perdre du temps ?
Quelle syntaxe ai-je cherchée ?
Quel bug a duré trop longtemps ?
Quel livrable ai-je commencé trop tard ?
Qu’est-ce que je peux automatiser mentalement ?
```

---

# 56. Plan B

Si un composant secondaire ne fonctionne pas :

```text
documenter proprement
```

Exemple :

```text
La base et l’ingestion sont fonctionnelles.
L’interface d’administration n’a pas pu être finalisée
dans le temps imparti.
```

Ne jamais masquer un problème.

---

# 57. Plan C

Si un composant majeur ne fonctionne pas :

```text
réduire le scope
```

Exemple :

```text
relation N-N complexe
→ simplifier en 1-N
si le sujet et les données le permettent
```

Toujours rester fidèle au besoin réel.

---

# 58. Script mental de départ

À 00:00 :

```text
1. Je lis tout.
2. Je liste les livrables.
3. Je choisis le chemin critique.
4. Je commence simple.
5. Je teste chaque phase.
6. Je garde 5 minutes pour rendre.
```

---

# 59. Script mental à mi-parcours

À 02:00 :

```text
Ai-je :
- un ETL fonctionnel ?
- une DB créée ?
- un ORM fonctionnel ?
```

Si non :

```text
simplifier immédiatement
```

---

# 60. Script mental à 03:00

```text
Ai-je :
- ingestion ?
- modèle entraîné ?
- score ?
- joblib ?
```

Si non :

```text
aucune amélioration secondaire
```

---

# 61. Script mental à 03:40

```text
plus aucun nouveau chantier
```

Uniquement :

```text
tests finaux
documentation
archive
```

---

# 62. Script mental à 03:55

```text
STOP CODING
```

Puis :

```text
VERIFY
ZIP
UPLOAD
```

---

# 63. Cheatsheet temps

```text
0:00  READ
0:15  EXPLORE
0:45  ETL
1:20  ORM
2:00  INGEST
2:30  ML
3:00  COMPOSE
3:25  TEST
3:40  DOC
3:55  ZIP
4:00  DONE
```

---

# 64. Résumé final

La difficulté du Bloc 2 n’est pas seulement technique.

Elle repose sur :

```text
largeur du périmètre
+
4 heures
+
surveillance
+
livrables multiples
```

La stratégie proposée est donc :

```text
COMPRENDRE
   ↓
PRIORIZER
   ↓
CONSTRUIRE SIMPLE
   ↓
TESTER TÔT
   ↓
CHANGER DE PHASE À L’HEURE
   ↓
DOCUMENTER
   ↓
LIVRER AVANT 4 H
```

Le principe ultime :

> **À 4 heures, seul le rendu livré compte.**

---

# 65. Document suivant

```text
10_RNCP_38919_BLOC_2_CHECKLIST_JOUR_J.md
```

Objectif :

> condenser la stratégie en checklist opérationnelle :
> veille de l’examen, 30 minutes avant, démarrage Mereos,
> checkpoints techniques, vérification du rendu et upload final.
