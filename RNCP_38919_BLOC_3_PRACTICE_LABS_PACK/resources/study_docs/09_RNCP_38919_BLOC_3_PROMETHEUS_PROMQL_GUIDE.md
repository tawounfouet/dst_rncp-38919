# 09 — RNCP 38919 — Bloc 3
# Guide Prometheus et PromQL

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Convention**
>
> - **Attendu source** : élément explicitement annoncé dans le support DataScientest.
> - **Guide pratique** : exemples de configuration, requêtes PromQL et mini-labs proposés pour la préparation.
>
> Le support annonce explicitement :
>
> ```text
> Prometheus
> prometheus-fastapi-instrumentator
> config/prometheus.yml
> PromQL
> ```
>
> Il ne fournit pas, dans la page source, une liste de métriques ou de requêtes PromQL précises à reproduire.
> Les exemples ci-dessous sont donc des **patterns de pratique**.

---

# 1. Position de Prometheus dans le Bloc 3

## Attendu source

Le support cite :

```text
Prometheus
```

avec :

```text
prometheus-fastapi-instrumentator
config/prometheus.yml
PromQL
```

## Modèle mental

```text
FastAPI
   ↓
prometheus-fastapi-instrumentator
   ↓
/metrics
   ↓
Prometheus
   ↓
PromQL
   ↓
Grafana
```

---

# 2. Rôle de Prometheus

## Guide pratique

Prometheus sert à :

```text
scraper des métriques
les stocker sous forme de séries temporelles
les interroger via PromQL
```

Dans le contexte du Bloc 3 :

```text
FastAPI
→ expose des métriques
→ Prometheus les collecte
→ Grafana les visualise
```

---

# 3. `prometheus-fastapi-instrumentator`

## Attendu source

Le support cite explicitement :

```text
prometheus-fastapi-instrumentator
```

## Guide pratique

Pattern de base :

```python
from fastapi import FastAPI

from prometheus_fastapi_instrumentator import (
    Instrumentator,
)


app = FastAPI()


Instrumentator().instrument(
    app
).expose(
    app
)
```

---

# 4. Endpoint `/metrics`

Avec une configuration de practice classique :

```text
GET /metrics
```

devient disponible.

Tester :

```bash
curl \
  http://localhost:8000/metrics
```

---

# 5. Pourquoi `/metrics`

Modèle :

```text
application
↓
endpoint de métriques
↓
Prometheus scrape
```

Prometheus ne "devine" pas l’état de l’application.

Il doit savoir :

```text
où
et
quoi
scraper
```

---

# 6. Vérifier FastAPI avant Prometheus

## Guide pratique

Avant de configurer Prometheus :

```bash
curl \
  http://localhost:8000/health
```

puis :

```bash
curl \
  http://localhost:8000/metrics
```

Si `/metrics` ne fonctionne pas :

```text
Prometheus ne pourra pas récupérer les métriques
```

---

# 7. `config/prometheus.yml`

## Attendu source

Le support cite explicitement :

```text
config/prometheus.yml
```

## Guide pratique

Structure minimale :

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: fastapi
    static_configs:
      - targets:
          - app:8000
```

---

# 8. `scrape_interval`

Pattern :

```yaml
global:
  scrape_interval: 15s
```

Signifie :

```text
Prometheus tente régulièrement
de récupérer les métriques
```

> La valeur `15s` est un exemple de pratique, pas une valeur imposée par le support.

---

# 9. `scrape_configs`

Pattern :

```yaml
scrape_configs:
  - job_name: fastapi
```

Le `job_name` permet de regrouper logiquement une cible.

---

# 10. `targets`

```yaml
static_configs:
  - targets:
      - app:8000
```

Dans Docker Compose :

```text
app
=
nom du service Docker
```

---

# 11. Erreur classique — `localhost`

Dans un container Prometheus :

```text
localhost
```

désigne généralement :

```text
le container Prometheus lui-même
```

et non :

```text
le container FastAPI
```

Donc en Compose :

```yaml
targets:
  - app:8000
```

est souvent le bon pattern si le service s’appelle :

```text
app
```

---

# 12. Docker Compose — FastAPI + Prometheus

## Guide pratique

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"

  prometheus:
    image: prom/prometheus
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    depends_on:
      - app
```

---

# 13. Démarrage

```bash
docker compose up \
  -d \
  --build
```

Vérifier :

```bash
docker compose ps
```

---

# 14. Logs Prometheus

```bash
docker compose logs \
  prometheus
```

Suivi :

```bash
docker compose logs \
  -f \
  prometheus
```

---

# 15. Interface Prometheus

## Guide pratique

Port de practice courant :

```text
9090
```

Donc :

```text
http://localhost:9090
```

> `9090` est un port conventionnel de pratique ; la page source ne fixe pas de port.

---

# 16. Vérifier la cible

Dans l’interface Prometheus, vérifier que la cible est :

```text
UP
```

Modèle de diagnostic :

```text
Target UP
→ scrape fonctionne

Target DOWN
→ problème de réseau / port / endpoint / config
```

---

# 17. Diagnostic cible DOWN

Vérifier dans cet ordre :

```text
1. app FastAPI démarrée ?
2. /metrics accessible ?
3. hostname correct ?
4. port correct ?
5. prometheus.yml monté ?
6. YAML valide ?
7. services sur le même réseau Compose ?
```

---

# 18. PromQL

## Attendu source

Le support cite explicitement :

```text
PromQL
```

## Guide pratique

PromQL est le langage de requête de Prometheus.

Il sert à :

```text
sélectionner
filtrer
agréger
calculer
```

des séries temporelles.

---

# 19. Requête la plus simple

Pattern :

```promql
metric_name
```

Exemple conceptuel :

```promql
http_requests_total
```

> Le nom exact des métriques dépend de l’application et de l’instrumentation.

---

# 20. Filtrer par label

Pattern :

```promql
metric_name{
  label="value"
}
```

Exemple conceptuel :

```promql
http_requests_total{
  method="GET"
}
```

---

# 21. Plusieurs labels

Pattern :

```promql
metric_name{
  method="GET",
  status="200"
}
```

---

# 22. Agrégation avec `sum`

```promql
sum(
  metric_name
)
```

---

# 23. Agrégation par label

```promql
sum by (method) (
  metric_name
)
```

---

# 24. `rate`

Pattern de practice :

```promql
rate(
  metric_name[5m]
)
```

Modèle mental :

```text
compteur cumulé
↓
rate
↓
vitesse d’évolution
```

---

# 25. Pourquoi `rate`

Un compteur qui augmente :

```text
100
101
102
103
```

peut être difficile à lire directement.

Avec :

```promql
rate(...)
```

on observe plutôt :

```text
la fréquence d’événements
```

---

# 26. `sum(rate(...))`

Pattern :

```promql
sum(
  rate(
    metric_name[5m]
  )
)
```

---

# 27. `sum by (...)`

Pattern :

```promql
sum by (method) (
  rate(
    metric_name[5m]
  )
)
```

---

# 28. Fenêtre temporelle

Exemple :

```promql
rate(
  metric_name[1m]
)
```

ou :

```promql
rate(
  metric_name[5m]
)
```

Le choix dépend :

```text
du niveau de lissage
et
du besoin d’analyse
```

---

# 29. Métriques à reconnaître conceptuellement

## Guide pratique

Le support ne donne pas de liste de métriques.

Dans les labs, entraînez-vous à reconnaître les familles :

```text
requêtes HTTP
latence
status codes
compteurs
process
Python
```

---

# 30. Compteur

Concept :

```text
counter
```

Exemple générique :

```text
nombre total de requêtes
```

Le compteur :

```text
augmente
```

et ne sert pas directement à exprimer un débit sans transformation.

---

# 31. Gauge

Concept de pratique :

```text
gauge
```

Exemple :

```text
valeur qui peut monter ou descendre
```

> Les types de métriques ne sont pas détaillés dans la page source ; ils sont ajoutés pour comprendre PromQL.

---

# 32. Histogramme

Concept de pratique :

```text
histogram
```

utile pour :

```text
durées
latences
distributions
```

> Non détaillé dans la source ; support pédagogique.

---

# 33. Observer les métriques réelles

Avant d’écrire une requête PromQL :

```bash
curl \
  http://localhost:8000/metrics
```

Puis identifier :

```text
noms exacts
labels disponibles
```

Réflexe important :

```text
ne pas inventer un nom de métrique
```

---

# 34. Explorer dans Prometheus

## Guide pratique

Dans l’UI Prometheus :

```text
Graph / Query
```

taper :

```promql
<metric_name>
```

puis exécuter.

---

# 35. Requête par méthode HTTP

Si une métrique expose un label :

```text
method
```

pattern :

```promql
sum by (method) (
  rate(
    metric_name[5m]
  )
)
```

---

# 36. Requête par status code

Si un label contient le status :

```promql
sum by (status) (
  rate(
    metric_name[5m]
  )
)
```

---

# 37. Requête par endpoint

Si les métriques exposent un label d’handler / path :

```promql
sum by (handler) (
  rate(
    metric_name[5m]
  )
)
```

Le nom réel du label dépend des métriques disponibles.

---

# 38. Interprétation avant syntaxe

## Guide pratique

Toujours partir d’une question :

```text
Combien de requêtes ?
À quel rythme ?
Par méthode ?
Par route ?
Quelle latence ?
Quels codes d’erreur ?
```

Puis construire la requête.

---

# 39. PromQL — démarche de construction

```text
1. metric_name
2. ajouter filtre label
3. ajouter rate si compteur
4. ajouter sum
5. ajouter group by
```

Exemple abstrait :

```promql
sum by (method) (
  rate(
    metric_name{
      status="200"
    }[5m]
  )
)
```

---

# 40. Erreur PromQL — métrique inconnue

Si aucune donnée :

```text
vérifier le nom exact de la métrique
```

avec :

```text
/metrics
ou
autocomplete Prometheus
```

---

# 41. Erreur PromQL — mauvais label

Si :

```promql
metric_name{
  method="GET"
}
```

ne retourne rien :

```text
le label method
peut ne pas exister
ou
avoir une autre valeur
```

---

# 42. Erreur PromQL — `rate` mal ciblé

`rate` est principalement destiné aux séries de type compteur.

Réflexe :

```text
comprendre la métrique
avant d’appliquer rate
```

---

# 43. Prometheus + Docker Compose

Architecture :

```text
Docker network
│
├── app:8000
│    └── /metrics
│
└── prometheus:9090
     └── scrape app:8000
```

---

# 44. Prometheus + Kubernetes

## Guide pratique

Le support annonce séparément :

```text
Kubernetes
Prometheus
```

La page source ne précise pas la méthode de déploiement de Prometheus dans Kubernetes.

Pour la préparation, retenez surtout le principe :

```text
Prometheus
→ doit joindre
→ une cible exposant des métriques
```

sans imposer une méthode Kubernetes non décrite dans la source.

---

# 45. Config Prometheus complète de practice

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: fastapi

    static_configs:
      - targets:
          - app:8000
```

---

# 46. Ajouter un deuxième job

Pattern :

```yaml
scrape_configs:
  - job_name: fastapi
    static_configs:
      - targets:
          - app:8000

  - job_name: another-service
    static_configs:
      - targets:
          - another-service:9000
```

> Exemple de pratique, non demandé explicitement.

---

# 47. Vérifier le YAML

## Guide pratique

Les erreurs fréquentes :

```text
indentation
:
-
target mal placé
job_name incorrectement indenté
```

---

# 48. Redémarrer Prometheus après config

Pattern :

```bash
docker compose restart \
  prometheus
```

ou :

```bash
docker compose down
docker compose up -d
```

selon votre environnement.

---

# 49. Prometheus dans le pipeline mental

```text
CODE
 ↓
FastAPI
 ↓
metrics
 ↓
Prometheus config
 ↓
scrape
 ↓
PromQL
```

---

# 50. Prometheus vs Grafana

Ne pas confondre :

```text
Prometheus
=
collecte + stockage + requêtes

Grafana
=
visualisation / dashboards
```

---

# 51. PromQL vs Grafana

```text
PromQL
=
langage de requête

Grafana
=
outil qui peut utiliser
des requêtes PromQL
pour afficher des panels
```

---

# 52. Mini-lab 1 — instrumenter FastAPI

Créer :

```text
GET /health
```

Puis ajouter :

```text
prometheus-fastapi-instrumentator
```

Vérifier :

```bash
curl \
  http://localhost:8000/metrics
```

---

# 53. Mini-lab 2 — config Prometheus

Créer :

```text
config/prometheus.yml
```

avec un job :

```text
fastapi
```

qui cible :

```text
app:8000
```

---

# 54. Mini-lab 3 — Compose

Créer :

```text
app
+
prometheus
```

Puis :

```bash
docker compose up -d
```

---

# 55. Mini-lab 4 — Target UP

Dans Prometheus :

```text
vérifier que la cible est UP
```

Si elle est DOWN :

```text
corriger sans toucher à Grafana
```

---

# 56. Mini-lab 5 — générer du trafic

Exécuter plusieurs fois :

```bash
curl \
  http://localhost:8000/health
```

Puis observer l’évolution des métriques.

---

# 57. Mini-lab 6 — première requête

Dans Prometheus :

```text
identifier une métrique réellement présente
```

Puis l’exécuter sans filtre.

---

# 58. Mini-lab 7 — filtrer

Trouver un label disponible.

Écrire :

```promql
metric_name{
  label="value"
}
```

---

# 59. Mini-lab 8 — rate

Sur une métrique compteur adaptée :

```promql
rate(
  metric_name[5m]
)
```

---

# 60. Mini-lab 9 — agrégation

```promql
sum(
  rate(
    metric_name[5m]
  )
)
```

---

# 61. Mini-lab 10 — group by

```promql
sum by (label) (
  rate(
    metric_name[5m]
  )
)
```

---

# 62. Mini-lab 11 — panne volontaire

Modifier :

```yaml
targets:
  - wrong-service:8000
```

Observer :

```text
target DOWN
```

Puis diagnostiquer.

---

# 63. Mini-lab 12 — port incorrect

Passer volontairement :

```text
8000
→ 9999
```

Observer le comportement.

Puis corriger.

---

# 64. Mini-lab 13 — `/metrics` absent

Désactiver temporairement l’instrumentation.

Observer :

```text
scrape impossible / réponse inattendue
```

Puis réactiver.

---

# 65. Checklist de maîtrise

```text
[ ] instrumenter FastAPI
[ ] accéder à /metrics
[ ] créer config/prometheus.yml
[ ] définir scrape_configs
[ ] définir une target
[ ] lancer Prometheus
[ ] vérifier target UP
[ ] identifier une métrique réelle
[ ] filtrer par label
[ ] utiliser rate
[ ] utiliser sum
[ ] utiliser sum by
[ ] diagnostiquer target DOWN
```

---

# 66. Diagnostic 60 secondes

```text
/metrics fonctionne ?
        ↓
prometheus.yml correct ?
        ↓
hostname correct ?
        ↓
port correct ?
        ↓
target UP ?
        ↓
metric existe ?
        ↓
labels corrects ?
```

---

# 67. Questions flash

1. Quel outil de monitoring est explicitement annoncé ?
2. Quelle librairie relie FastAPI à Prometheus ?
3. Quel fichier de configuration est explicitement cité ?
4. Quel langage de requête est explicitement cité ?
5. À quoi sert `/metrics` ?
6. Qu’est-ce qu’une target Prometheus ?
7. Que signifie `UP` ?
8. Pourquoi `localhost` peut-il être faux dans Compose ?
9. À quoi sert `rate()` ?
10. À quoi sert `sum by (...)` ?
11. Que faire avant d’inventer une requête PromQL ?
12. Quelle différence entre Prometheus et Grafana ?

---

# 68. Réponses flash

```text
1. Prometheus.
2. prometheus-fastapi-instrumentator.
3. config/prometheus.yml.
4. PromQL.
5. exposer les métriques de l’application.
6. endpoint / service que Prometheus scrape.
7. la collecte fonctionne.
8. localhost désigne le container courant.
9. calculer un taux d’évolution sur une série adaptée.
10. agréger tout en regroupant par label.
11. vérifier les métriques et labels réellement exposés.
12. Prometheus collecte/interroge ; Grafana visualise.
```

---

# 69. Cheatsheet 30 secondes

FastAPI :

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(
    app
).expose(
    app
)
```

Prometheus :

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: fastapi
    static_configs:
      - targets:
          - app:8000
```

PromQL :

```promql
metric_name
```

```promql
metric_name{
  label="value"
}
```

```promql
rate(
  metric_name[5m]
)
```

```promql
sum by (label) (
  rate(
    metric_name[5m]
  )
)
```

---

# 70. Fil rouge à retenir

```text
FASTAPI
   ↓
INSTRUMENTATOR
   ↓
/METRICS
   ↓
PROMETHEUS
   ↓
PROMQL
```

Puis :

```text
PROMQL
   ↓
GRAFANA
```

---

# 71. Document suivant

```text
10_RNCP_38919_BLOC_3_GRAFANA_GUIDE.md
```

Objectif :

> approfondir la dernière brique d’observabilité annoncée :
> configuration d’une datasource Prometheus via
> `datasources/<source_name>.yml`
> et création de dashboards depuis l’interface Grafana.
