# 04 — RNCP 38919 — Bloc 3
# Guide GitLab, CI/CD et Runner `shell`

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Convention**
>
> - **Attendu source** : élément explicitement annoncé dans le support DataScientest.
> - **Guide pratique** : commandes, exemples YAML et exercices proposés pour réviser.
>
> Le support annonce explicitement :
>
> ```text
> GitLab
> Repository
> .gitlab-ci.yml
> pipeline
> Runner
> gitlab-runner
> clé SSH
> repository privé dst_rncp38919_bloc_3
> Runner de type shell nommé shell
> ```
>
> Le support ne détaille pas, dans la page fournie, le contenu exact du pipeline à construire pendant l’examen.
> Les exemples de pipeline de ce document sont donc des **patterns de préparation**.

---

# 1. Position de GitLab dans le Bloc 3

## Attendu source

Le support demande de maîtriser :

```text
GitLab
├── Repository
├── .gitlab-ci.yml
└── Runner
```

Le modèle mental à retenir est :

```text
Code
 ↓
Repository GitLab
 ↓
.gitlab-ci.yml
 ↓
Pipeline
 ↓
Job
 ↓
Runner
 ↓
Shell de la VM
```

---

# 2. Préparation GitLab avant l’examen

## Attendu source

Le support demande de créer :

```text
un compte GitLab
```

puis un repository privé nommé exactement :

```text
dst_rncp38919_bloc_3
```

Cette préparation doit être réalisée **avant** le passage.

---

# 3. Pourquoi préparer le repository avant le jour J

## Analyse

Le Bloc 3 dure 4 heures.

Créer pendant l’épreuve :

```text
compte
repository
SSH
Runner
```

ferait perdre du temps sur des prérequis déjà annoncés à l’avance.

Réflexe :

```text
PREPARE BEFORE
→ EXECUTE DURING
```

---

# 4. Créer un repository GitLab

## Guide pratique

Depuis GitLab :

```text
New project
↓
Create blank project
↓
Project name
↓
dst_rncp38919_bloc_3
↓
Visibility
↓
Private
```

Le support exige explicitement le nom :

```text
dst_rncp38919_bloc_3
```

---

# 5. Git — initialiser un projet local

## Guide pratique

```bash
git init
```

Puis :

```bash
git status
```

---

# 6. Ajouter les fichiers

```bash
git add .
```

Vérifier :

```bash
git status
```

---

# 7. Premier commit

```bash
git commit \
  -m "Initial commit"
```

---

# 8. Définir la branche principale

Pattern de pratique :

```bash
git branch -M main
```

Le support ne fixe pas le nom de branche dans la page fournie.

---

# 9. Ajouter un remote GitLab

Exemple SSH :

```bash
git remote add origin \
  git@gitlab.com:USER/dst_rncp38919_bloc_3.git
```

Vérifier :

```bash
git remote -v
```

---

# 10. Push initial

```bash
git push \
  -u origin main
```

---

# 11. SSH — exigence du support

## Attendu source

Le support demande :

```text
créer une clé SSH sur la machine virtuelle
```

puis :

```text
ajouter la clé publique générée
au compte GitLab
```

---

# 12. Générer une clé SSH

## Guide pratique

Pattern courant :

```bash
ssh-keygen \
  -t ed25519 \
  -C "email@example.com"
```

> Le support n’impose pas dans la page fournie le type de clé `ed25519`.
> Il s’agit d’un exemple de pratique courant.

---

# 13. Lire la clé publique

```bash
cat ~/.ssh/id_ed25519.pub
```

Copier ensuite le contenu dans GitLab.

---

# 14. Ajouter la clé dans GitLab

## Guide pratique

Chemin conceptuel :

```text
GitLab
→ Preferences / Settings
→ SSH Keys
→ Add new key
```

Le libellé exact de l’interface peut évoluer.

---

# 15. Tester SSH

Pattern :

```bash
ssh -T git@gitlab.com
```

Objectif :

```text
vérifier que l'authentification GitLab fonctionne
```

---

# 16. Le fichier `.gitlab-ci.yml`

## Attendu source

Le support demande :

```text
la création d’un pipeline
à l’aide du fichier .gitlab-ci.yml
```

Ce fichier se place à la racine du repository :

```text
project/
├── .gitlab-ci.yml
├── src/
├── tests/
└── ...
```

---

# 17. Rôle du `.gitlab-ci.yml`

## Guide pratique

Il décrit :

```text
stages
jobs
scripts
variables éventuelles
conditions éventuelles
```

Le modèle mental :

```text
YAML
↓
GitLab lit le fichier
↓
pipeline généré
↓
jobs distribués
↓
runner exécute
```

---

# 18. Pipeline minimal de préparation

## Guide pratique

```yaml
stages:
  - test

test:
  stage: test
  script:
    - pytest -v
```

Cela signifie :

```text
stage : test
job   : test
script: pytest -v
```

> Exemple de préparation, non imposé par le support.

---

# 19. Plusieurs stages

Pattern :

```yaml
stages:
  - test
  - build
  - deploy
```

Ordre :

```text
test
 ↓
build
 ↓
deploy
```

---

# 20. Job de test

```yaml
test:
  stage: test
  script:
    - python --version
    - pytest -v
```

---

# 21. Job de build Docker

```yaml
build:
  stage: build
  script:
    - docker build -t my-app:latest .
```

Le support annonce à la fois GitLab CI et Docker ; ce pattern permet de les relier pour l’entraînement.

---

# 22. Job de push DockerHub

Pattern de pratique :

```yaml
push:
  stage: deploy
  script:
    - docker tag my-app:latest USER/my-app:latest
    - docker push USER/my-app:latest
```

> La page source n’impose pas un job DockerHub précis dans `.gitlab-ci.yml`.

---

# 23. Variables dans GitLab CI

## Guide pratique

Dans YAML :

```yaml
variables:
  APP_ENV: "test"
```

Dans un script :

```yaml
script:
  - echo "$APP_ENV"
```

---

# 24. Secrets CI/CD

## Guide pratique

Ne pas écrire dans le repository :

```text
password DockerHub
token DockerHub
secret API
```

Préférer des variables protégées / masquées dans l’interface GitLab lorsque cela est applicable.

> La page source n’entre pas dans le détail de la gestion des secrets GitLab ; ce point est une bonne pratique de préparation.

---

# 25. GitLab Runner — exigence du support

## Attendu source

Le support demande de créer :

```text
un Runner de type shell
```

nommé :

```text
shell
```

Puis de l’enregistrer sur :

```text
la machine virtuelle
```

---

# 26. Rôle du Runner

## Guide pratique

```text
GitLab
→ crée le job

Runner
→ récupère le job

Shell executor
→ exécute les commandes sur la VM
```

---

# 27. Pourquoi le Runner `shell` compte

Avec un Runner `shell` :

```text
les commandes du job
s’exécutent directement
dans le shell de la VM
```

Donc l’environnement de la VM doit disposer de ce dont le job a besoin :

```text
Python
pytest
Docker
Git
etc.
```

---

# 28. `gitlab-runner`

## Attendu source

Le support cite explicitement :

```text
gitlab-runner
```

## Guide pratique

Vérifier :

```bash
gitlab-runner --version
```

Lister :

```bash
gitlab-runner list
```

---

# 29. Enregistrement du Runner

## Guide pratique

Le support demande de l’enregistrer sur la VM.

La commande exacte dépend de la méthode / version GitLab, mais le concept à retenir est :

```text
GitLab crée / configure le Runner
        ↓
un token / mécanisme d’enregistrement est fourni
        ↓
gitlab-runner enregistre la VM
        ↓
executor = shell
```

Ne pas mémoriser aveuglément une ancienne syntaxe d’enregistrement si l’interface GitLab en affiche une différente le jour de la préparation.

---

# 30. Runner online

Avant l’examen, vérifier dans GitLab :

```text
Runner
→ online / active
```

et côté VM :

```bash
gitlab-runner list
```

---

# 31. Runner et tags

## Guide pratique

Certains pipelines peuvent cibler un Runner avec :

```yaml
tags:
  - shell
```

Mais :

> le support indique le **nom** du Runner `shell`, sans préciser dans la page fournie qu’un tag `shell` sera obligatoire.

Il ne faut donc pas confondre automatiquement :

```text
nom du Runner
```

et :

```text
tag du Runner
```

---

# 32. Première CI à tester avant l’examen

## Stratégie de préparation

Créer un pipeline ultra-simple :

```yaml
stages:
  - test

hello:
  stage: test
  script:
    - echo "Runner OK"
    - python --version
```

Objectif :

```text
push
↓
pipeline
↓
job
↓
Runner shell
↓
success
```

---

# 33. Chaîne de validation du Runner

```text
1. commit .gitlab-ci.yml
2. push
3. ouvrir CI/CD
4. observer pipeline
5. ouvrir job
6. lire logs
7. vérifier runner utilisé
```

---

# 34. Ajouter Pytest au pipeline

```yaml
stages:
  - test

tests:
  stage: test
  script:
    - pytest -v
```

---

# 35. Environnement virtuel dans un Runner shell

## Guide pratique

Deux stratégies de practice :

### A. dépendances déjà installées sur la VM

```yaml
script:
  - pytest -v
```

### B. créer un venv pendant le job

```yaml
script:
  - python -m venv .venv
  - source .venv/bin/activate
  - pip install -r requirements.txt
  - pytest -v
```

Le support ne prescrit pas une méthode unique.

---

# 36. Pipeline avec test + build

```yaml
stages:
  - test
  - build

tests:
  stage: test
  script:
    - pytest -v

docker_build:
  stage: build
  script:
    - docker build -t my-app:latest .
```

---

# 37. Dépendance logique des stages

Si :

```text
test échoue
```

alors le stage suivant n’est généralement pas exécuté dans un pipeline standard.

Modèle :

```text
TEST KO
→ STOP

TEST OK
→ BUILD
```

---

# 38. Logs CI

## Réflexe de debug

Toujours lire :

```text
la première vraie erreur
```

et non seulement :

```text
Job failed
```

Regarder :

```text
commande exécutée
exit code
stdout
stderr
```

---

# 39. Erreur — Runner absent

Symptôme typique :

```text
job pending
```

Questions :

```text
Runner online ?
Runner assigné au projet ?
tag compatible ?
Runner paused ?
```

---

# 40. Erreur — commande introuvable

Exemple :

```text
pytest: command not found
```

Cela indique généralement que le shell Runner ne voit pas l’outil.

Vérifier :

```bash
which pytest
which python
```

ou installer les dépendances dans le job.

---

# 41. Erreur — Docker inaccessible

Exemple conceptuel :

```text
docker: command not found
```

ou :

```text
permission denied
```

Vérifier :

```bash
docker --version
docker ps
```

dans le même environnement utilisateur que le Runner.

---

# 42. Runner shell et contexte utilisateur

## Guide pratique

Le Runner peut s’exécuter sous un utilisateur système différent de votre session interactive.

Conséquence possible :

```text
PATH différent
permissions différentes
variables différentes
```

D’où l’intérêt de vérifier dans le job :

```yaml
script:
  - whoami
  - pwd
  - env
```

> Ce point est une aide de debug générale ; il n’est pas détaillé dans la page source.

---

# 43. `before_script`

## Guide pratique

Pattern :

```yaml
before_script:
  - python --version
```

Puis :

```yaml
tests:
  script:
    - pytest -v
```

> Cette clé n’est pas explicitement citée dans le support. Elle est incluse ici comme syntaxe GitLab CI utile pour les entraînements.

---

# 44. `artifacts`

## Guide pratique

Pattern possible :

```yaml
tests:
  stage: test
  script:
    - pytest -v
  artifacts:
    paths:
      - reports/
```

> `artifacts` n’est pas cité dans la page source. À considérer comme extension facultative de pratique.

---

# 45. Pipeline Bloc 3 de référence pour practice

```yaml
stages:
  - test
  - build

tests:
  stage: test
  script:
    - python --version
    - pytest -v

build_image:
  stage: build
  script:
    - docker build -t rncp-bloc3:latest .
```

Ce fichier est suffisant pour pratiquer :

```text
Repository
.gitlab-ci.yml
Pipeline
Runner
Docker
```

---

# 46. GitLab CI + DockerHub — pratique avancée

Pattern :

```yaml
stages:
  - test
  - build
  - push

tests:
  stage: test
  script:
    - pytest -v

build:
  stage: build
  script:
    - docker build -t rncp-bloc3 .

push:
  stage: push
  script:
    - echo "$DOCKERHUB_TOKEN" | docker login \
        -u "$DOCKERHUB_USER" \
        --password-stdin
    - docker tag rncp-bloc3 \
        "$DOCKERHUB_USER/rncp-bloc3:latest"
    - docker push \
        "$DOCKERHUB_USER/rncp-bloc3:latest"
```

> Pattern de révision construit à partir des thèmes GitLab + DockerHub annoncés dans le support.

---

# 47. Ne jamais committer les tokens

À éviter :

```yaml
DOCKERHUB_TOKEN: "abc123..."
```

dans le repository.

Préférer :

```text
GitLab CI/CD Variables
```

si ce mécanisme est utilisé.

---

# 48. Repository — structure de practice

```text
dst_rncp38919_bloc_3/
│
├── app/
│   └── ...
│
├── tests/
│   └── ...
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitlab-ci.yml
└── README.md
```

---

# 49. Workflow quotidien

```text
modifier
↓
tester localement
↓
git add
↓
git commit
↓
git push
↓
pipeline
↓
logs
```

---

# 50. GitLab vs Runner

Ne pas confondre :

```text
GitLab
=
orchestrateur / plateforme

Runner
=
agent d'exécution
```

---

# 51. Pipeline vs Job

```text
Pipeline
=
ensemble d’exécutions liées à un commit

Job
=
unité de travail
```

---

# 52. Stage vs Job

```text
Stage
=
phase logique

Job
=
tâche exécutée dans cette phase
```

Exemple :

```text
stage test
├── unit_tests
└── api_tests
```

---

# 53. Commit qui déclenche un pipeline

## Guide pratique

Typiquement :

```bash
git add .
git commit -m "Add CI"
git push
```

Puis GitLab détecte :

```text
.gitlab-ci.yml
```

et crée le pipeline.

---

# 54. Vérifier l’historique

```bash
git log \
  --oneline
```

---

# 55. Vérifier la branche

```bash
git branch
```

---

# 56. Vérifier le remote

```bash
git remote -v
```

---

# 57. Vérifier le statut

```bash
git status
```

---

# 58. Mini-lab 1 — Repository

## Mission

Créer un repo local :

```text
bloc3-ci-practice
```

Puis :

```text
README.md
app.py
tests/
.gitgitignore
```

Faire :

```text
init
add
commit
push
```

---

# 59. Mini-lab 2 — SSH

## Mission

Vérifier :

```text
push via SSH
```

sans saisir à chaque fois :

```text
username / password HTTP
```

---

# 60. Mini-lab 3 — Runner hello world

Créer :

```yaml
stages:
  - test

hello:
  stage: test
  script:
    - echo "Runner shell OK"
    - whoami
    - pwd
```

Objectif :

```text
pipeline vert
```

---

# 61. Mini-lab 4 — Runner Python

Ajouter :

```yaml
script:
  - python --version
  - python -c "print('Python OK')"
```

---

# 62. Mini-lab 5 — Pytest CI

Créer :

```python
def test_health():
    assert 1 + 1 == 2
```

Pipeline :

```yaml
tests:
  stage: test
  script:
    - pytest -v
```

---

# 63. Mini-lab 6 — Pipeline cassé

Modifier volontairement :

```python
assert 1 + 1 == 3
```

Observer :

```text
pipeline rouge
job log
exit code
```

Puis corriger.

---

# 64. Mini-lab 7 — Build Docker

Ajouter un Dockerfile minimal.

Pipeline :

```yaml
build:
  stage: build
  script:
    - docker build -t bloc3-demo .
```

---

# 65. Mini-lab 8 — End-to-end GitLab

Objectif :

```text
commit
↓
push
↓
pytest
↓
docker build
↓
pipeline vert
```

---

# 66. Mini-lab 9 — DockerHub

Si votre compte est prêt :

```text
build
↓
tag
↓
login
↓
push
```

Puis vérifier l’image dans DockerHub.

---

# 67. Debug — pipeline YAML invalide

Vérifier :

```text
indentation
:
-
nom de stage
nom de job
script
```

GitLab peut signaler un fichier CI invalide avant même l’exécution des jobs.

---

# 68. Debug — mauvais stage

Exemple :

```yaml
job:
  stage: deploy
```

alors que :

```yaml
stages:
  - test
  - build
```

Le job référence un stage non déclaré.

---

# 69. Debug — mauvais répertoire

Dans un Runner shell :

```bash
pwd
ls -la
```

permettent de vérifier où le job s’exécute.

---

# 70. Debug — variables absentes

Dans un job de practice :

```yaml
script:
  - env | sort
```

Attention à ne pas afficher volontairement de secrets dans des logs réels.

---

# 71. Diagnostic Runner 60 secondes

```text
Pipeline pending ?
      ↓
Runner online ?
      ↓
Runner associé au projet ?
      ↓
tag compatible ?
      ↓
executor shell ?
      ↓
commande disponible ?
```

---

# 72. Checklist avant l’examen

## Source + préparation

```text
[ ] repository privé dst_rncp38919_bloc_3
[ ] clone SSH fonctionne
[ ] push SSH fonctionne
[ ] Runner shell créé
[ ] Runner enregistré sur la VM
[ ] Runner online
[ ] pipeline hello-world déjà testé
[ ] pytest fonctionne depuis le Runner
[ ] Docker fonctionne depuis le Runner
```

Les cinq premiers éléments sont directement liés aux prérequis annoncés dans le support ; les tests hello-world / pytest / Docker sont des vérifications de préparation proposées.

---

# 73. Questions flash

1. Quel repository faut-il créer avant l’examen ?
2. Quelle visibilité ?
3. Pourquoi créer une clé SSH ?
4. Quel fichier définit la CI GitLab ?
5. Qu’est-ce qu’un pipeline ?
6. Qu’est-ce qu’un job ?
7. Qu’est-ce qu’un stage ?
8. Quel est le rôle d’un Runner ?
9. Quel type de Runner est demandé ?
10. Quel nom est demandé ?
11. Où s’exécutent les commandes d’un Runner shell ?
12. Que vérifier si un job reste `pending` ?
13. Pourquoi tester `pytest` depuis le Runner avant l’examen ?
14. Pourquoi ne pas committer un token DockerHub ?

---

# 74. Réponses flash

```text
1. dst_rncp38919_bloc_3.
2. privé.
3. authentifier la VM auprès de GitLab.
4. .gitlab-ci.yml.
5. ensemble des jobs associés à une exécution CI/CD.
6. unité de travail.
7. phase logique du pipeline.
8. exécuter les jobs.
9. shell.
10. shell.
11. directement dans le shell / environnement de la VM.
12. runner online, association, tags, état du runner.
13. éviter de découvrir un problème d’environnement pendant l’épreuve.
14. protéger les credentials.
```

---

# 75. Cheatsheet 30 secondes

```bash
git status
git add .
git commit -m "message"
git push

ssh -T git@gitlab.com

gitlab-runner --version
gitlab-runner list
```

`.gitlab-ci.yml` :

```yaml
stages:
  - test
  - build

tests:
  stage: test
  script:
    - pytest -v

build:
  stage: build
  script:
    - docker build -t app .
```

---

# 76. Fil rouge à retenir

```text
CODE
 ↓
GIT PUSH
 ↓
GITLAB
 ↓
PIPELINE
 ↓
RUNNER SHELL
 ↓
PYTEST
 ↓
DOCKER BUILD
```

---

# 77. Document suivant

```text
05_RNCP_38919_BLOC_3_DOCKER_DOCKERHUB_GUIDE.md
```

Objectif :

> approfondir Docker, `Dockerfile`, volumes, `docker-compose.yml`,
> `services.depends_on`, DockerHub et le cycle build → tag → push.
