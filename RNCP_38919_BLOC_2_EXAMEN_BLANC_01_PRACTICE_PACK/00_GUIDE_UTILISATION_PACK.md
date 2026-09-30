# Guide d’utilisation

## Mode apprentissage

Travaillez les labs dans l’ordre :

```text
LAB 01 — JSON / Jupyter / pandas
LAB 02 — ETL Python
LAB 03 — Docker Compose / DB
LAB 04 — SQLAlchemy ORM
LAB 05 — Ingestion + tests
LAB 06 — ML + joblib
LAB 07 — End-to-End
```

Chaque lab contient :
- `README.md` : énoncé ;
- `starter/` : point de départ ;
- `solution/` : solution de référence.

## Mode examen blanc

Ouvrez uniquement :

```text
exam/sujet/
exam/starter_project/
```

Chronomètre :

```text
4:00:00
```

Ne consultez la correction qu’après la fin.

## Source vs choix de préparation

Le support principal DataScientest mentionne une base relationnelle Docker administrée via
`phpMyAdmin`. Le support ORM dédié illustre PostgreSQL + pgAdmin. Le mock exam de ce pack
utilise **MariaDB + phpMyAdmin** pour rester cohérent avec le support principal, tandis que
les concepts ORM restent génériques SQLAlchemy.
