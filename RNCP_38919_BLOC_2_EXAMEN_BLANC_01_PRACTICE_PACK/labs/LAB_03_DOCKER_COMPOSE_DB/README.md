# LAB 03 — Docker Compose, MariaDB et phpMyAdmin

**Temps cible : 30 min**

## Objectifs
- déclarer une DB relationnelle ;
- utiliser `.env` ;
- exposer les ports ;
- créer un volume persistant ;
- lancer phpMyAdmin ;
- savoir diagnostiquer avec `docker compose ps` et `docker compose logs`.

## Check
```bash
docker compose up -d
docker compose ps
docker compose logs db
```

Puis ouvrez phpMyAdmin sur le port configuré.
