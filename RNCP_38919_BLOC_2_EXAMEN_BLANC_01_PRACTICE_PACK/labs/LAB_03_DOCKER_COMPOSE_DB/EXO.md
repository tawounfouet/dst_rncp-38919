# LAB 03 — Mode examen

⏱ **30 min**. Écrivez le `docker-compose.yml` de zéro dans `starter/`.

## Checklist chronométrée

- [ ] 0–6 : service `db` (image `mariadb:11`)
- [ ] 6–14 : variables d'environnement via `.env`
- [ ] 14–19 : ports + volume
- [ ] 19–25 : service `phpMyAdmin` + `depends_on`
- [ ] 25–30 : `up`, `ps`, `logs`, connexion

## Questions de contrôle

1. Pourquoi un volume plutôt que les données dans le conteneur ?
2. Que fait `depends_on` — et que **ne** fait-il pas ?
3. À quoi sert `${DB_NAME}` dans le compose ?

## Solution

<details>
<summary>docker-compose.yml</summary>

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
</details>

<details>
<summary>.env</summary>

```dotenv
DB_PORT=3306
DB_NAME=practice
DB_USER=practice_user
DB_PASSWORD=practice_password
DB_ROOT_PASSWORD=root_password
PMA_PORT=8080
```
</details>

<details>
<summary>Commandes de diagnostic</summary>

```bash
docker compose up -d
docker compose ps
docker compose logs db
docker compose exec db mariadb -upractice_user -ppractice_password practice -e "SHOW DATABASES;"
```
</details>

## Pièges

- `depends_on` **ne garantit pas** que la DB est prête → erreurs de connexion
  si on enchaîne tout de suite (LAB 04). Solution : `healthcheck`.
- Oublier le volume → données perdues à chaque `down`.
- `MARIADB_*` (et non `MYSQL_*`) pour l'image `mariadb`.
- Le port **interne** reste `3306` ; seul le port hôte change.

## Auto-évaluation

| Point | OK ? |
|---|---|
| Je monte une DB + admin en compose | |
| J'externalise tout dans `.env` | |
| Je sais créer et expliquer un volume | |
| Je diagnostique avec `ps` / `logs` / `exec` | |
