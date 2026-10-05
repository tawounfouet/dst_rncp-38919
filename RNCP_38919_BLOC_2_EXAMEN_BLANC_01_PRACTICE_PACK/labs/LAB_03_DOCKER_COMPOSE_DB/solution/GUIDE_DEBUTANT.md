# LAB 03 — Guide débutant (de zéro à la solution)

> **Public** : tu n'as jamais utilisé Docker. Aucun prérequis technique.
> On explique **chaque** mot (image, conteneur, volume…) au moment où il apparaît.
> À la fin, tu auras une base de données MariaDB et phpMyAdmin qui tournent.

---

## Étape 0 — Le vocabulaire Docker

| Mot | Signification simple |
|---|---|
| **Docker** | Un outil qui fait tourner des logiciels dans des « boîtes » isolées, sans les installer sur ta machine. |
| **Image** | Le **modèle** figé d'un logiciel (ex. `mariadb:11` = MariaDB version 11). On la télécharge. |
| **Conteneur** | Une **instance en cours d'exécution** d'une image (l'image devient un conteneur qui tourne). |
| **Compose** | Un fichier qui décrit **plusieurs conteneurs** à lancer ensemble. |
| **Service** | Un conteneur décrit dans `docker-compose.yml` (ici `db` et `phpmyadmin`). |
| **Volume** | Un espace de **stockage qui survit** à l'arrêt du conteneur (sinon les données sont perdues). |
| **Port** | La « porte » par laquelle on accède au service. `8080:80` = dehors `8080` → dedans `80`. |
| **`mariadb` / `mysql`** | Deux bases de données relationnelles très proches (presque le même langage SQL). |
| **phpMyAdmin** | Une interface web pour **voir** la base dans un navigateur. |

Le but de ce lab : lancer une base + son interface, sans rien installer « en dur ».

---

## Étape 1 — Vérifier que Docker est installé

```bash
docker --version
docker compose version
```

Attendu : une version de Docker et de Docker Compose (v2). Sinon, installe **Docker Desktop**.

---

## Étape 2 — Le fichier `.env` : la configuration

Un fichier **`.env`** contient des **variables** sous forme `CLE=valeur`. On le recopie depuis l'exemple :

```bash
cd LAB_03_DOCKER_COMPOSE_DB/solution
cp .env.example .env
```

Contenu de `.env` :

```dotenv
DB_PORT=3306
DB_NAME=practice
DB_USER=practice_user
DB_PASSWORD=practice_password
DB_ROOT_PASSWORD=root_password
PMA_PORT=8080
```

- **Pourquoi un `.env` ?** Pour **ne pas écrire les mots de passe dans le code ou dans le compose**. On les sépare : le `.env` est propre à ta machine et n'est **pas** partagé (souvent dans `.gitignore`).
- `.env.example` = le modèle à recopier ; il ne contient pas de vrai secret.

---

## Étape 3 — Le fichier `docker-compose.yml`

C'est lui qui décrit les conteneurs. Voici la solution :

```yaml
services:
  db:
    image: mariadb:11
    environment:
      MARIADB_DATABASE: ${DB_NAME}
      MARIADB_USER: ${DB_USER}
      MARIADB_PASSWORD: ${DB_PASSWORD}
      MARIADB_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    ports:
      - "${DB_PORT}:3306"
    volumes:
      - db_data:/var/lib/mysql

  phpmyadmin:
    image: phpmyadmin:latest
    environment:
      PMA_HOST: db
      PMA_PORT: 3306
    ports:
      - "${PMA_PORT}:80"
    depends_on:
      - db

volumes:
  db_data:
```

Décryptage **notion par notion** :

- `services:` → la liste des conteneurs à lancer.
- `db:` → nom du premier service (notre base de données).
- `image: mariadb:11` → l'image utilisée (`mariadb`, version `11`). Docker la télécharge la 1re fois.
- `environment:` → les **variables d'environnement** passées au conteneur. `${DB_NAME}` est **remplacé** par la valeur lue dans le `.env`. C'est le lien entre les deux fichiers !
  - `MARIADB_DATABASE` → nom de la base créée automatiquement.
  - `MARIADB_USER` / `MARIADB_PASSWORD` → le compte applicatif.
  - `MARIADB_ROOT_PASSWORD` → le mot de passe administrateur.
  - ⚠️ L'image `mariadb` attend des variables préfixées **`MARIADB_`** (pas `MYSQL_`).
- `ports: - "${DB_PORT}:3306"` → **mapping de ports**. À gauche le port **de ta machine** (`DB_PORT`, ex. 3306), à droite le port **dans le conteneur** (3306, fixe pour MariaDB). Donc `3306:3306` = « le 3306 de mon Mac pointe vers le 3306 du conteneur ».
- `volumes: - db_data:/var/lib/mysql` → `/var/lib/mysql` est le dossier **où MariaDB stocke ses données** dans le conteneur ; on le branche sur un volume nommé `db_data`. **Sans ça, toutes les données disparaissent à chaque arrêt.**
- `phpmyadmin:` → second service.
  - `image: phpmyadmin:latest` → l'interface web.
  - `PMA_HOST: db` → **à l'intérieur du réseau Docker, on joint la base par son nom de service** `db` (pas `localhost` !). C'est une erreur classique de mettre `localhost`.
  - `ports: - "${PMA_PORT}:80"` → l'interface écoute sur le port 80 dans le conteneur ; on l'expose sur `8080` chez toi.
  - `depends_on: - db` → ordre de démarrage : phpMyAdmin attend que `db` soit lancé. ⚠️ **Attention** : `depends_on` ne garantit **pas** que la base est *prête* à recevoir des connexions, seulement que le conteneur est démarré.
- `volumes:` (tout en bas, au même niveau que `services:`) → déclaration du volume nommé `db_data`.

---

## Étape 4 — Lancer

```bash
docker compose up -d
```

- `up` → crée et démarre les conteneurs.
- `-d` → **detached** : en arrière-plan (le terminal reste libre).

Vérifier :

```bash
docker compose ps
```

Attendu :

```text
db          Up   0.0.0.0:3306->3306/tcp
phpmyadmin  Up   0.0.0.0:8080->80/tcp
```

Voir les journaux (si ça ne marche pas) :

```bash
docker compose logs db
```

---

## Étape 5 — Vérifier que la base répond

```bash
docker compose exec db mariadb -upractice_user -ppractice_password practice -e "SELECT VERSION();"
```

- `exec db ...` → **exécute une commande dans le conteneur `db`**.
- `mariadb -u<user> -p<pass> <base>` → le client de base de données (user, mot de passe, nom de base).
- `-e "SELECT VERSION();"` → exécute cette requête SQL et affiche le résultat.

Attendu : `11.8.x-MariaDB-...`. C'est la **preuve** que la base est opérationnelle.

Ouvre ensuite phpMyAdmin : <http://localhost:8080>
(serveur `db`, utilisateur `practice_user`, mot de passe `practice_password`).

---

## Étape 6 — Arrêter / nettoyer

```bash
docker compose down        # arrête les conteneurs, GARDE les données (volume)
docker compose down -v     # arrête ET SUPPRIME le volume (repart de zéro)
```

- `down` → stoppe et supprime les conteneurs.
- `-v` → supprime aussi les **volumes** (donc les données). Utile pour repartir propre.

---

## Erreurs fréquentes

| Message | Cause | Solution |
|---|---|---|
| `ports are not available ... address already in use` | un autre MySQL/MariaDB occupe déjà 3306 | change `DB_PORT=3307` dans `.env` et relance |
| `no configuration file provided` | lancé hors du dossier | `cd` dans le dossier contenant `docker-compose.yml` |
| phpMyAdmin « cannot connect » | base pas encore prête | attends ~10 s, regarde `docker compose logs db` |
| `PMA_HOST` erreur | `localhost` au lieu du nom de service | utiliser `db` |
| données perdues à l'arrêt | pas de volume | ajouter `db_data:/var/lib/mysql` |

---

## Pour aller plus loin (notions vues)

```text
image       → modèle figé d'un logiciel
conteneur   → instance en cours d'une image
service     → conteneur décrit dans le compose
port        → "hôte:conteneur"
volume      → stockage persistant
.env        → variables de configuration hors du code
depends_on  → ordre de démarrage (pas de "prêt")
```

> **Lien avec le LAB 04** : la base créée ici sera utilisée par l'ORM.
> Si tu changes `DB_PORT`, note-le : il faudra la même valeur dans le LAB 04.
