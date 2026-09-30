# 05 — RNCP 38919 — Bloc 2
# Guide Docker & Docker Compose

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 2 — Projet ETL & ML  
**Durée officielle :** 4 heures

**Sources principales :**
- `Examen RNCP 38919 _ Bloc 2 - Projet ETL & ML.pdf`
- `Examen RNCP 38919 _ Bloc 2 - ORM.pdf`

> **Règle de lecture**
>
> - **Attendu source** : élément explicitement présent dans les supports fournis.
> - **Guide pratique** : exemple de préparation construit à partir de cet attendu.
>
> Les supports fournis ne sont pas totalement homogènes sur le moteur / outil d’administration :
>
> - le support principal du Bloc 2 mentionne une **base relationnelle avec Docker** et une administration via **phpMyAdmin** ;
> - le support ORM montre un environnement **PostgreSQL + pgAdmin** via Docker Compose.
>
> Ce document ne cherche pas à corriger ou fusionner artificiellement ces deux supports.
> Il se concentre sur les compétences Docker / Compose communes aux deux, puis montre le cas PostgreSQL + pgAdmin parce qu’il apparaît explicitement dans la ressource ORM.
> Le jour de l’examen, il faudra suivre la stack effectivement demandée dans le sujet.

---

# 1. Ce que le Bloc 2 attend sur Docker

## Attendu source

Le support principal indique qu’il faut savoir :

```text
- lancer des conteneurs via docker run ;
- créer et exécuter un fichier docker-compose.yml ;
- monter des volumes pour la persistance des données ;
- configurer des variables d’environnement pour sécuriser les services.
```

Il annonce également :

```text
création d’une base de données relationnelle avec Docker
```

et :

```text
mise en place d’un environnement de production
pour la collecte et l’ingestion de données
via docker-compose
```

La préparation Docker doit donc couvrir au minimum :

```text
container
image
port
environment
volume
service
compose
logs
démarrage / arrêt
```

---

# 2. Modèle mental Docker

## Guide pratique

```text
Dockerfile
   ↓
Image
   ↓
Container
   ↓
Service en exécution
```

Avec Compose :

```text
docker-compose.yml
        │
        ├── database
        ├── admin UI
        └── application / ingestion
```

---

# 3. Image vs Container

## Guide pratique

```text
IMAGE
=
modèle immuable utilisé pour créer un container

CONTAINER
=
instance en exécution d'une image
```

Commandes :

```bash
docker images
docker ps
docker ps -a
```

---

# 4. Commandes Docker de base

## Guide pratique

Lister les containers actifs :

```bash
docker ps
```

Tous les containers :

```bash
docker ps -a
```

Lister les images :

```bash
docker images
```

Logs :

```bash
docker logs <container>
```

Logs en continu :

```bash
docker logs -f <container>
```

Arrêter :

```bash
docker stop <container>
```

Supprimer :

```bash
docker rm <container>
```

Supprimer une image :

```bash
docker rmi <image>
```

Entrer dans un container :

```bash
docker exec -it <container> sh
```

ou, si Bash existe :

```bash
docker exec -it <container> bash
```

---

# 5. `docker run`

## Attendu source

Le support principal demande de savoir :

```text
lancer des conteneurs via docker run
```

## Guide pratique

Exemple générique :

```bash
docker run -d \
  --name my-container \
  -p 8080:80 \
  my-image
```

À retenir :

```text
-d
→ arrière-plan

--name
→ nom du container

-p host:container
→ mapping de port
```

---

# 6. Ports

## Guide pratique

Syntaxe :

```text
HOST:CONTAINER
```

Exemple :

```yaml
ports:
  - "5432:5432"
```

Signifie :

```text
localhost:5432
      ↓
container:5432
```

Réflexe de debug :

```text
Le service écoute-t-il réellement sur le port interne ?
Le port host est-il déjà utilisé ?
Le mapping est-il correct ?
```

---

# 7. Variables d’environnement

## Attendu source

Le support principal cite explicitement les variables d’environnement dans :

```text
les fichiers Docker
et
les scripts Python
```

## Guide pratique

### Fichier `.env`

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=app
DB_USER=app
DB_PASSWORD=secret
```

### Docker Compose

```yaml
environment:
  POSTGRES_DB: ${DB_NAME}
  POSTGRES_USER: ${DB_USER}
  POSTGRES_PASSWORD: ${DB_PASSWORD}
```

### Python

```python
import os

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
```

Réflexe :

```text
Code
≠
Configuration
≠
Secrets
```

---

# 8. Volumes

## Attendu source

Le support principal demande de savoir :

```text
monter des volumes
pour la persistance des données
```

## Guide pratique

Sans volume :

```text
container supprimé
→ données potentiellement perdues
```

Avec volume :

```text
container supprimé
→ volume conservé
→ données persistantes
```

Exemple :

```yaml
services:
  db:
    image: postgres:16-alpine
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

---

# 9. Bind mount vs Volume

## Guide pratique

Volume nommé :

```yaml
volumes:
  - db_data:/var/lib/postgresql/data
```

Bind mount :

```yaml
volumes:
  - ./data:/app/data
```

Différence mentale :

```text
volume nommé
→ géré par Docker

bind mount
→ répertoire local directement monté
```

Le support principal exige la compréhension de la persistance, pas une préférence obligatoire entre les deux dans la page fournie.

---

# 10. Docker Compose — commandes essentielles

## Attendu source

Le support demande de savoir :

```text
créer et exécuter un fichier docker-compose.yml
```

## Guide pratique

Démarrer :

```bash
docker compose up -d
```

État :

```bash
docker compose ps
```

Logs :

```bash
docker compose logs
```

Logs continus :

```bash
docker compose logs -f
```

Arrêter et supprimer les containers du projet :

```bash
docker compose down
```

Rebuild :

```bash
docker compose up -d --build
```

---

# 11. Structure minimale d’un Compose

## Guide pratique

```yaml
services:
  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

Concepts à reconnaître immédiatement :

```text
services
image
ports
environment
volumes
```

---

# 12. `depends_on`

## Attendu source

Le support principal indique l’utilisation de `docker-compose` pour l’environnement de collecte / ingestion.

## Guide pratique

Lorsque l’application dépend de la base :

```yaml
services:
  app:
    build: .
    depends_on:
      - db
```

Modèle mental :

```text
app
 ↓
depends_on
 ↓
db
```

Important :

```text
depends_on
ne garantit pas toujours
que la base est déjà prête
à accepter des connexions
```

Ce point relève du comportement général de Compose et constitue une aide de préparation ; la page source fournie n’entre pas dans ce niveau de détail.

---

# 13. Cas du support ORM : PostgreSQL + pgAdmin

## Attendu source

Le support ORM fournit un environnement Compose contenant :

```text
PostgreSQL
+
pgAdmin
```

Il utilise notamment l’image :

```yaml
postgres:16-alpine
```

et :

```yaml
dpage/pgadmin4
```

Les ports visibles dans le support sont :

```text
PostgreSQL : 5432
pgAdmin    : 5050 → 80
```

---

# 14. Exemple PostgreSQL + pgAdmin aligné sur le support ORM

## Guide pratique

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: daniel
      POSTGRES_PASSWORD: datascientest
      POSTGRES_DB: dst_db
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db

volumes:
  db_data:
```

> Cet exemple reprend la logique du support ORM.
> Les valeurs exactes du sujet d’examen devront être utilisées le jour J.

---

# 15. Connexion SQLAlchemy depuis le poste hôte

## Source + guide pratique

Le support ORM utilise une URL de type :

```text
postgresql+psycopg://
USER:PASSWORD@localhost:5432/DATABASE
```

Exemple :

```python
DATABASE_URL = (
    "postgresql+psycopg://"
    "daniel:datascientest"
    "@localhost:5432/dst_db"
)
```

Ici :

```text
localhost
```

est cohérent lorsque le script Python s’exécute sur le poste hôte et PostgreSQL expose :

```text
5432:5432
```

---

# 16. Connexion entre containers

## Guide pratique

Si l’application Python est elle-même dans Compose :

```yaml
services:
  app:
    ...
  db:
    ...
```

alors le hostname est généralement le nom du service :

```text
db
```

et non :

```text
localhost
```

Donc :

```env
DB_HOST=db
```

Modèle mental :

```text
Depuis le poste hôte
→ localhost:5432

Depuis un autre container du Compose
→ db:5432
```

---

# 17. Erreur classique : `localhost`

## Guide pratique

Dans un container :

```text
localhost
=
ce container lui-même
```

Donc :

```text
app container
localhost:5432
```

ne désigne pas automatiquement :

```text
db container
```

Réflexe :

```text
service name
=
hostname interne Compose
```

---

# 18. Réseau Compose

## Guide pratique

Dans un même projet Compose :

```text
app
 ↕
db
 ↕
admin
```

les services peuvent communiquer via leurs noms de service.

Exemple :

```text
db:5432
```

---

# 19. Exemple d’application d’ingestion

## Guide pratique

Architecture de préparation :

```text
data.json
   │
   ▼
app / ingestion
   │
   ▼
PostgreSQL
```

Compose :

```yaml
services:
  db:
    image: postgres:16-alpine
    ...

  ingest:
    build: .
    depends_on:
      - db
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: app
      DB_USER: app
      DB_PASSWORD: secret
```

---

# 20. Dockerfile minimal pour un script Python

## Guide pratique

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/ingest.py"]
```

Le support principal mentionne Docker et Compose ; la page fournie ne fixe pas ce Dockerfile précis.

---

# 21. `requirements.txt`

## Guide pratique

Pour une stack proche du Bloc 2 :

```text
pandas
sqlalchemy
psycopg[binary]
scikit-learn
joblib
matplotlib
pytest
```

À adapter au sujet.

---

# 22. Compose avec `build`

## Guide pratique

```yaml
services:
  ingest:
    build: .
```

Cela indique :

```text
Compose
→ construit l’image
à partir du Dockerfile
```

---

# 23. Ordre de démarrage

## Guide pratique

```text
docker compose up -d
        ↓
docker compose ps
        ↓
docker compose logs
        ↓
tester DB
        ↓
tester application
```

Ne pas commencer par déboguer le code Python avant d’avoir vérifié que les services sont réellement démarrés.

---

# 24. Vérifier PostgreSQL

## Guide pratique

Avec Docker :

```bash
docker compose ps
```

Puis :

```bash
docker compose logs db
```

Si nécessaire :

```bash
docker exec -it <db-container> sh
```

---

# 25. Vérifier l’administration graphique

## Source

Le support ORM utilise pgAdmin.

Après démarrage :

```text
http://localhost:5050
```

est cohérent avec un mapping :

```yaml
- "5050:80"
```

Le support principal, lui, mentionne phpMyAdmin.
Il faut donc suivre l’outil effectivement fourni ou demandé dans le sujet réel.

---

# 26. Source mismatch à retenir

## Attendu source

Les deux supports montrent :

```text
Support principal
→ phpMyAdmin

Support ORM
→ PostgreSQL + pgAdmin
```

Conclusion de préparation :

```text
Ne pas déduire avant le sujet
qu'un moteur précis sera forcément utilisé.
```

Ce qu’il faut vraiment maîtriser :

```text
Docker
Compose
ports
volumes
env vars
base relationnelle
outil d’administration
connexion Python
```

---

# 27. Debug — container ne démarre pas

## Guide pratique

Ordre :

```text
1. docker compose ps
2. docker compose logs <service>
3. vérifier YAML
4. vérifier image
5. vérifier ports
6. vérifier variables
7. vérifier volumes
```

Commande :

```bash
docker compose logs db
```

---

# 28. Debug — port déjà occupé

## Guide pratique

Symptôme :

```text
bind:
address already in use
```

Réflexes :

```text
quel processus utilise le port ?
un ancien container tourne-t-il ?
le mapping host doit-il changer ?
```

Lister :

```bash
docker ps
```

---

# 29. Debug — mauvais mot de passe

## Guide pratique

Vérifier que ces valeurs correspondent :

```text
Compose
.env
Python
SQLAlchemy URL
outil admin
```

Anti-pattern :

```text
DB_PASSWORD différent
dans 3 fichiers
```

---

# 30. Debug — volume persistant avec ancien état

## Guide pratique

Cas classique :

```text
je modifie POSTGRES_PASSWORD
mais la base réutilise un volume
déjà initialisé
```

Le volume conserve l’ancien état.

Réflexe :

```text
ne pas supprimer les volumes
sans comprendre les conséquences
```

Pour un exercice jetable uniquement, on peut parfois repartir de zéro.

---

# 31. `docker compose down`

## Guide pratique

```bash
docker compose down
```

supprime les containers / réseau du projet, mais les volumes nommés persistent généralement.

Pour supprimer aussi les volumes :

```bash
docker compose down -v
```

Attention :

```text
-v
=
destructif pour les données persistées
```

---

# 32. Debug — application ne voit pas la DB

Checklist :

```text
[ ] les deux services sont actifs
[ ] même projet / réseau Compose
[ ] DB_HOST = nom du service
[ ] DB_PORT = port interne
[ ] credentials corrects
[ ] database correcte
[ ] driver installé
```

---

# 33. Healthcheck — préparation avancée

## Guide pratique

Le support n’impose pas explicitement de healthcheck dans la page fournie.

Mais pour comprendre un environnement robuste :

```yaml
services:
  db:
    image: postgres:16-alpine
    healthcheck:
      test:
        [
          "CMD-SHELL",
          "pg_isready -U ${DB_USER} -d ${DB_NAME}"
        ]
      interval: 5s
      timeout: 5s
      retries: 10
```

À connaître comme amélioration possible, pas comme exigence source.

---

# 34. Compose d’entraînement complet

## Guide pratique

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "${DB_PORT}:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD}
    ports:
      - "5050:80"
    depends_on:
      - db

  ingest:
    build: .
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
    depends_on:
      - db

volumes:
  db_data:
```

---

# 35. `.env` correspondant

```env
DB_NAME=dst_db
DB_USER=daniel
DB_PASSWORD=datascientest
DB_PORT=5432

PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin
```

---

# 36. URL SQLAlchemy depuis `ingest`

## Guide pratique

```python
import os

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
```

---

# 37. Ne pas exposer les secrets dans le code

## Guide pratique

Éviter :

```python
PASSWORD = "datascientest"
```

dans plusieurs scripts.

Préférer :

```python
os.getenv("DB_PASSWORD")
```

Le support principal cite explicitement les variables d’environnement dans les scripts Python et les fichiers Docker.

---

# 38. Organisation de projet proposée

## Guide pratique

```text
project/
│
├── src/
│   ├── database.py
│   └── ingest.py
│
├── data/
│   └── raw/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── .env
├── requirements.txt
└── README.md
```

---

# 39. Flow de démarrage recommandé

```text
1. créer .env
2. créer docker-compose.yml
3. docker compose up -d
4. docker compose ps
5. docker compose logs db
6. tester connexion
7. exécuter ORM
8. exécuter ingestion
```

---

# 40. Flow de nettoyage recommandé

```text
docker compose down
```

Puis uniquement si environnement jetable et besoin réel :

```text
docker compose down -v
```

---

# 41. Mini-exercice 1 — `docker run`

Objectif :

```text
lancer un container simple
avec un port exposé
```

Vérifier :

```bash
docker ps
```

Puis arrêter :

```bash
docker stop ...
```

---

# 42. Mini-exercice 2 — PostgreSQL seul

Créer un Compose avec :

```text
1 service PostgreSQL
1 volume
3 variables :
- DB
- USER
- PASSWORD
```

Vérifier :

```text
container UP
port 5432 accessible
logs sans erreur
```

---

# 43. Mini-exercice 3 — pgAdmin

Ajouter :

```text
pgAdmin
```

Vérifier :

```text
localhost:5050
```

Puis connecter pgAdmin au service PostgreSQL.

---

# 44. Mini-exercice 4 — Persistance

Étapes :

```text
1. démarrer DB
2. créer une table / donnée
3. docker compose down
4. docker compose up -d
5. vérifier que la donnée existe encore
```

Objectif :

```text
comprendre réellement le volume
```

---

# 45. Mini-exercice 5 — Variables d’environnement

Remplacer les valeurs codées en dur par :

```text
.env
```

Puis utiliser :

```yaml
${DB_NAME}
${DB_USER}
${DB_PASSWORD}
```

---

# 46. Mini-exercice 6 — App Python + DB

Créer :

```text
db
+
ingest
```

Le script `ingest` doit se connecter à :

```text
db:5432
```

et non :

```text
localhost:5432
```

lorsqu’il s’exécute lui-même dans un container.

---

# 47. Mini-exercice 7 — Pipeline complet

Objectif :

```text
JSON
 ↓
pandas
 ↓
SQLAlchemy
 ↓
PostgreSQL container
```

Puis vérifier les données via l’outil d’administration.

---

# 48. Anti-patterns

## 1. Tout mettre sur `localhost`

Dans Compose :

```text
container A → localhost
```

ne signifie pas :

```text
container B
```

---

## 2. Supprimer les volumes sans réfléchir

```bash
docker compose down -v
```

peut supprimer les données de l’exercice.

---

## 3. Mettre les secrets dans Git

Éviter de versionner :

```text
.env
```

avec des secrets réels.

---

## 4. Ignorer les logs

Avant de modifier du code :

```bash
docker compose logs
```

---

## 5. Utiliser `depends_on` comme garantie de disponibilité

Un service peut être démarré sans être encore prêt à répondre.

---

# 49. Checklist Docker avant examen blanc

```text
[ ] docker installé
[ ] docker compose fonctionne
[ ] je sais lancer un container
[ ] je sais voir les containers
[ ] je sais lire les logs
[ ] je sais exposer un port
[ ] je sais déclarer un volume
[ ] je sais utiliser .env
[ ] je sais relier app → db
[ ] je sais arrêter proprement
```

---

# 50. Checklist debug 60 secondes

```text
SERVICE KO ?
   ↓
docker compose ps
   ↓
docker compose logs SERVICE
   ↓
PORT ?
ENV ?
HOST ?
PASSWORD ?
VOLUME ?
DRIVER ?
```

---

# 51. Révision flash

À réciter :

```text
docker ps
docker logs
docker compose up -d
docker compose ps
docker compose logs
docker compose down

ports
volumes
environment
depends_on
service-name-as-hostname
```

---

# 52. Questions flash

1. Différence entre image et container ?
2. À quoi sert `-p` ?
3. À quoi sert un volume ?
4. Comment lancer Compose en arrière-plan ?
5. Comment lire les logs ?
6. Pourquoi utiliser `.env` ?
7. Dans Compose, quel hostname utiliser pour joindre le service `db` ?
8. Pourquoi `localhost` peut être faux dans un container ?
9. Que fait `docker compose down` ?
10. Que risque `docker compose down -v` ?
11. Quelle stack DB/admin apparaît dans le support ORM ?
12. Quelle autre interface admin est citée dans le support principal ?

---

# 53. Réponses flash

```text
1. image = modèle ; container = instance exécutée.
2. mapper un port host vers un port container.
3. persister des données.
4. docker compose up -d.
5. docker compose logs.
6. séparer configuration / secrets du code.
7. db.
8. localhost désigne le container courant.
9. arrête / supprime les containers du projet et son réseau.
10. suppression des volumes / données persistées.
11. PostgreSQL + pgAdmin.
12. phpMyAdmin.
```

---

# 54. Niveau attendu à viser

```text
NIVEAU 1
docker run
docker ps
logs

      ↓

NIVEAU 2
Compose
ports
environment
volumes

      ↓

NIVEAU 3
PostgreSQL / admin UI
connexion SQLAlchemy

      ↓

NIVEAU 4
app d’ingestion
→ DB containerisée
```

---

# 55. Checkpoint avant Machine Learning

Avant de passer à la partie ML, être capable d’avoir :

```text
[ ] base démarrée
[ ] volume présent
[ ] variables env correctes
[ ] connexion SQLAlchemy OK
[ ] tables ORM créées
[ ] ingestion fonctionnelle
[ ] données vérifiables
```

---

# 56. Résumé final

Le périmètre Docker du Bloc 2 repose sur cinq réflexes :

```text
RUN
 ↓
CONFIGURE
 ↓
PERSIST
 ↓
CONNECT
 ↓
DEBUG
```

Traduction :

```text
docker run
docker compose
variables d’environnement
volumes
réseau / hostname
logs
```

La finalité n’est pas simplement de lancer une base.

Elle est de rendre possible :

```text
collecte / transformation
        ↓
application Python
        ↓
base relationnelle containerisée
        ↓
ingestion reproductible
```

dans le cadre du mini-projet Bloc 2.

---

# 57. Document suivant

```text
06_RNCP_38919_BLOC_2_MACHINE_LEARNING_GUIDE.md
```

Objectif :

> approfondir uniquement la partie Machine Learning annoncée dans le support :
> préparation des données, entraînement avec `scikit-learn`,
> évaluation et sauvegarde du modèle avec `joblib`.
