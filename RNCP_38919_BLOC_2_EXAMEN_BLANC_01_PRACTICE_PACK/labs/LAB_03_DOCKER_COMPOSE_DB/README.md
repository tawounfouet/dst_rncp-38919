# LAB 03 — Docker Compose, MariaDB et phpMyAdmin

**Temps cible : 30 min** · Difficulté : ⭐⭐ · Prérequis : Docker

## Objectifs

- déclarer une DB relationnelle avec Docker Compose ;
- externaliser la configuration dans un `.env` ;
- exposer les ports ;
- créer un **volume persistant** ;
- lancer phpMyAdmin ;
- diagnostiquer avec `docker compose ps` et `docker compose logs`.

## Contenu

```text
LAB_03_DOCKER_COMPOSE_DB/
├── starter/
│   ├── docker-compose.yml   # TODO à compléter
│   └── .env.example
├── solution/
│   ├── docker-compose.yml   # MariaDB 11 + phpMyAdmin
│   └── .env.example
├── EXO.md
└── README.md
```

## Lancement

```bash
cd LAB_03_DOCKER_COMPOSE_DB/solution
cp .env.example .env
docker compose up -d
docker compose ps
docker compose logs db
```

Attendu dans `docker compose ps` :

```text
NAME                     IMAGE              STATUS         PORTS
...-db-1                 mariadb:11         Up ...         0.0.0.0:3306->3306/tcp
...-phpmyadmin-1         phpmyadmin:latest  Up ...         0.0.0.0:8080->80/tcp
```

Puis ouvrez phpMyAdmin : <http://localhost:8080> (serveur `db`, utilisateur
`practice_user`, mot de passe `practice_password`).

Test rapide en CLI :

```bash
docker compose exec db mariadb -upractice_user -ppractice_password practice -e "SELECT VERSION();"
```

## Variables (`.env`)

| Variable | Défaut | Rôle |
|---|---|---|
| `DB_PORT` | `3306` | port exposé sur l'hôte |
| `DB_NAME` | `practice` | base créée au démarrage |
| `DB_USER` / `DB_PASSWORD` | `practice_user` / `practice_password` | compte applicatif |
| `DB_ROOT_PASSWORD` | `root_password` | root MariaDB |
| `PMA_PORT` | `8080` | port HTTP de phpMyAdmin |

## Critères de réussite

- [ ] `docker compose ps` montre les 2 conteneurs `Up` ;
- [ ] `docker compose exec db mariadb ...` renvoie la version (11.x) ;
- [ ] phpMyAdmin répond sur <http://localhost:8080> ;
- [ ] les données survivent à `docker compose down` puis `up` (volume) ;
- [ ] `docker compose logs db` ne contient pas d'erreur fatale.

## Arrêt / nettoyage

```bash
docker compose down        # arrête, conserve le volume (données)
docker compose down -v     # arrête et SUPPRIME le volume (repart de zéro)
```

## Dépannage

| Symptôme | Cause | Correctif |
|---|---|---|
| `ports are not available ... address already in use` | un MySQL/MariaDB local occupe déjà `3306` | changer `DB_PORT` dans `.env` (ex. `3307`) : `DB_PORT=3307` |
| `no configuration file provided` | lancé hors du dossier | `cd LAB_03_DOCKER_COMPOSE_DB/solution` |
| `config` renvoie une erreur | variable non définie | vérifier que `.env` existe (`cp .env.example .env`) |
| phpMyAdmin « cannot connect » | DB pas encore prête | attendre ~10 s, `docker compose logs db` |
| volume non pris en compte (Windows) | partage de fichiers Docker | activer le file sharing dans Docker Desktop |

> **Lien avec le LAB 04** : le LAB 04 se connecte à **cette** base. Si vous
> changez `DB_PORT` ici, reportez la même valeur dans le `.env` du LAB 04.

## Pour aller plus loin

- Ajouter un `healthcheck` sur `db` et `depends_on: condition: service_healthy`.
- Ajouter un service `adminer` en alternative légère à phpMyAdmin.
- Ajouter un script d'init SQL monté dans `/docker-entrypoint-initdb.d`.
