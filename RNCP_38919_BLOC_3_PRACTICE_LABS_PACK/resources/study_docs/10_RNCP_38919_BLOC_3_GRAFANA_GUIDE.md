# 10 — RNCP 38919 — Bloc 3
# Guide Grafana

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Convention**
>
> - **Attendu source** : élément explicitement annoncé dans le support DataScientest.
> - **Guide pratique** : exemples de configuration, dashboards et mini-labs proposés pour la préparation.
>
> Le support annonce explicitement :
>
> ```text
> Grafana
> configuration d’une source de données
> via datasources/<source_name>.yml
> création d’un dashboard depuis l’interface Grafana
> ```
>
> Il ne fournit pas, dans la page source :
>
> ```text
> un dashboard exact à reproduire
> un nombre de panels imposé
> une requête PromQL précise
> un thème Grafana
> une structure de provisioning complète
> ```
>
> Les exemples ci-dessous sont donc des **patterns de préparation**.

---

# 1. Position de Grafana dans le Bloc 3

## Attendu source

Le support cite :

```text
Grafana
```

avec deux compétences :

```text
1. configurer une source de données
   via datasources/<source_name>.yml

2. créer un dashboard
   depuis l’interface Grafana
```

## Modèle mental

```text
FastAPI
   ↓
/metrics
   ↓
Prometheus
   ↓
PromQL
   ↓
Grafana
   ↓
Dashboard
```

---

# 2. Rôle de Grafana

## Guide pratique

Grafana sert principalement à :

```text
visualiser des métriques
créer des panels
assembler des dashboards
explorer des données
```

Dans le Bloc 3 :

```text
Prometheus
=
source de métriques

Grafana
=
couche de visualisation
```

---

# 3. Grafana ne collecte pas les métriques

Modèle mental :

```text
FastAPI
→ expose

Prometheus
→ collecte

Grafana
→ affiche
```

Ne pas confondre :

```text
collecte
```

et :

```text
visualisation
```

---

# 4. Datasource Grafana

## Attendu source

Le support demande :

```text
configuration d’une source de données
via datasources/<source_name>.yml
```

Une datasource permet à Grafana de savoir :

```text
où se trouve Prometheus
```

---

# 5. Arborescence de practice

Pattern :

```text
grafana/
└── provisioning/
    └── datasources/
        └── prometheus.yml
```

> Le support cite `datasources/<source_name>.yml` mais ne fixe pas toute l’arborescence de provisioning.

---

# 6. Datasource Prometheus minimale

## Guide pratique

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

---

# 7. Champs essentiels

```text
name
type
url
```

Pattern :

```text
name
→ nom affiché dans Grafana

type
→ prometheus

url
→ adresse de Prometheus
```

---

# 8. `access: proxy`

Pattern de practice :

```yaml
access: proxy
```

Cela signifie que Grafana interroge la datasource depuis son propre contexte.

> Ce champ n’est pas détaillé dans la page source ; il est inclus comme pattern de provisioning courant.

---

# 9. `isDefault`

Pattern :

```yaml
isDefault: true
```

Cela permet de définir Prometheus comme datasource par défaut.

> Option de practice, non imposée par le support.

---

# 10. URL Prometheus dans Docker Compose

Si le service Compose s’appelle :

```text
prometheus
```

et écoute sur :

```text
9090
```

alors depuis Grafana :

```yaml
url: http://prometheus:9090
```

est un pattern cohérent.

---

# 11. Erreur classique — `localhost`

Dans un container Grafana :

```text
localhost
```

désigne :

```text
le container Grafana
```

et non Prometheus.

Donc dans Compose :

```text
http://prometheus:9090
```

est généralement plus cohérent si le service se nomme `prometheus`.

---

# 12. Docker Compose — Grafana + Prometheus

## Guide pratique

```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
```

---

# 13. Monter la datasource

Pattern :

```yaml
services:
  grafana:
    image: grafana/grafana
    volumes:
      - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
```

---

# 14. Compose complet de practice

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

  grafana:
    image: grafana/grafana
    volumes:
      - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
```

---

# 15. Démarrer la stack

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

# 16. Logs Grafana

```bash
docker compose logs \
  grafana
```

Suivi :

```bash
docker compose logs \
  -f \
  grafana
```

---

# 17. Accès Grafana

Port de practice courant :

```text
3000
```

Donc :

```text
http://localhost:3000
```

> `3000` est une convention de pratique fréquente, pas une valeur imposée par la source.

---

# 18. Vérifier la datasource

## Guide pratique

Dans Grafana :

```text
Connections
→ Data sources
→ Prometheus
```

Puis vérifier :

```text
URL
type
status
```

Le libellé exact de l’interface peut évoluer.

---

# 19. Test de datasource

Objectif :

```text
Grafana
→ peut joindre Prometheus
```

Si la datasource est correctement configurée :

```text
la connexion doit fonctionner
```

---

# 20. Dashboard — exigence du support

## Attendu source

Le support demande :

```text
création d’un dashboard
depuis l’interface Grafana
```

Il faut donc savoir utiliser :

```text
l’UI
```

et pas seulement provisionner une datasource en YAML.

---

# 21. Dashboard — modèle mental

```text
Dashboard
├── Panel 1
├── Panel 2
├── Panel 3
└── ...
```

Chaque panel contient typiquement :

```text
source de données
requête
visualisation
titre
```

---

# 22. Créer un dashboard

## Guide pratique

Chemin conceptuel :

```text
Dashboards
→ New
→ New dashboard
→ Add visualization
```

Le wording exact peut évoluer selon la version.

---

# 23. Sélectionner Prometheus

Dans un panel :

```text
Data source
→ Prometheus
```

Puis saisir une requête :

```text
PromQL
```

---

# 24. Premier panel

Pattern de practice :

```text
Titre
→ Requests

Datasource
→ Prometheus

Query
→ métrique HTTP existante
```

Important :

```text
utiliser une métrique réellement présente
```

---

# 25. Ne pas inventer les métriques

Avant de construire un panel :

```bash
curl \
  http://localhost:8000/metrics
```

ou explorer Prometheus.

Puis utiliser :

```text
les noms exacts
```

---

# 26. Panel de volume de requêtes

Pattern conceptuel :

```promql
sum(
  rate(
    metric_name[5m]
  )
)
```

> `metric_name` doit être remplacé par une métrique réellement exposée.

---

# 27. Panel par méthode HTTP

Si un label :

```text
method
```

existe :

```promql
sum by (method) (
  rate(
    metric_name[5m]
  )
)
```

---

# 28. Panel par status code

Si un label :

```text
status
```

existe :

```promql
sum by (status) (
  rate(
    metric_name[5m]
  )
)
```

---

# 29. Panel par route

Si un label de route existe :

```promql
sum by (handler) (
  rate(
    metric_name[5m]
  )
)
```

Le vrai nom du label dépend des métriques disponibles.

---

# 30. Panel de latence

## Guide pratique

Le support ne fournit pas de requête officielle.

Pour l’entraînement, si une métrique de durée est disponible :

```text
identifier ses noms / buckets / labels
```

puis construire une requête adaptée.

Ne pas mémoriser une requête sans vérifier :

```text
la métrique réelle
```

---

# 31. Types de visualisation

## Guide pratique

Grafana peut afficher différents types de panels.

Pour l’épreuve, garder une logique simple :

```text
Time series
Stat
Gauge
Table
```

> Le support ne fixe pas de type de panel précis.

---

# 32. `Time series`

À privilégier pour :

```text
évolution dans le temps
```

Exemple :

```text
requêtes par seconde
```

---

# 33. `Stat`

À privilégier pour :

```text
une valeur synthétique
```

Exemple :

```text
nombre courant
```

---

# 34. `Gauge`

À privilégier pour :

```text
visualiser une valeur par rapport à une plage
```

> Type de visualisation de practice, non imposé.

---

# 35. `Table`

Utile pour :

```text
afficher des dimensions
labels
valeurs détaillées
```

---

# 36. Titres de panels

## Guide pratique

Éviter :

```text
Panel 1
Panel 2
```

Préférer :

```text
HTTP Request Rate
Requests by Status
Requests by Method
```

---

# 37. Unités

Pattern :

```text
requests/s
seconds
milliseconds
count
```

Configurer une unité cohérente améliore la lisibilité.

> Bonne pratique de préparation, non exigence source.

---

# 38. Dashboard minimal de practice

Créer trois panels :

```text
1. Request rate
2. Requests by status
3. Requests by method
```

Cela suffit pour pratiquer :

```text
datasource
PromQL
panels
dashboard
```

---

# 39. Dashboard et trafic

Sans trafic :

```text
pas ou peu de données
```

Donc générer :

```bash
curl \
  http://localhost:8000/health
```

plusieurs fois.

---

# 40. Générer du trafic

Pattern Bash :

```bash
for i in {1..20}
do
  curl -s \
    http://localhost:8000/health \
    > /dev/null
done
```

> Boucle de practice, non issue du support.

---

# 41. Générer des POST

Pattern :

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"value": 42}' \
  http://localhost:8000/predict
```

Cela peut créer des métriques différentes selon les labels exposés.

---

# 42. Générer des erreurs

Pour tester un dashboard par status :

```bash
curl \
  -i \
  http://localhost:8000/unknown
```

Puis observer si les métriques exposées permettent de distinguer le code de statut.

---

# 43. Pipeline d’observabilité complet

```text
Request
 ↓
FastAPI
 ↓
Instrumentator
 ↓
/metrics
 ↓
Prometheus scrape
 ↓
PromQL
 ↓
Grafana panel
```

---

# 44. Debug datasource Grafana

Si Grafana ne joint pas Prometheus :

```text
URL correcte ?
service prometheus actif ?
port 9090 ?
réseau Compose ?
datasource provisionnée ?
```

---

# 45. Debug — datasource absente

Vérifier :

```text
chemin du volume
nom du fichier YAML
syntaxe YAML
logs Grafana
```

---

# 46. Debug — panel vide

Vérifier :

```text
Prometheus contient des données ?
requête PromQL valide ?
time range correct ?
métrique exacte ?
labels exacts ?
trafic généré ?
```

---

# 47. Debug — PromQL valide mais rien dans Grafana

Comparer la même requête dans :

```text
Prometheus UI
```

et :

```text
Grafana
```

Si elle fonctionne dans Prometheus mais pas Grafana :

```text
vérifier datasource et time range
```

---

# 48. Debug — mauvaise URL en Docker

Incorrect :

```yaml
url: http://localhost:9090
```

dans Grafana containerisé.

Pattern plus cohérent :

```yaml
url: http://prometheus:9090
```

si le service s’appelle `prometheus`.

---

# 49. Debug — YAML

Comme les autres fichiers Bloc 3, vérifier :

```text
indentation
:
-
chemins
noms de services
URL
```

---

# 50. Datasource — exemple complet de practice

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

> `editable` est un exemple de configuration complémentaire, non cité par la source.

---

# 51. Grafana dans Docker Compose — exemple complet

```yaml
grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
  volumes:
    - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
  depends_on:
    - prometheus
```

---

# 52. Structure de dossier de practice

```text
project/
│
├── app/
│
├── config/
│   └── prometheus.yml
│
├── grafana/
│   └── provisioning/
│       └── datasources/
│           └── prometheus.yml
│
├── docker-compose.yml
└── ...
```

---

# 53. Séquence de validation

## Guide pratique

```text
1. FastAPI répond
2. /metrics répond
3. Prometheus target = UP
4. PromQL retourne des données
5. Grafana datasource fonctionne
6. dashboard affiche les données
```

Ne pas commencer par Grafana si :

```text
Prometheus ne scrape pas
```

---

# 54. Mini-lab 1 — lancer Grafana

Ajouter :

```text
grafana
```

au Compose.

Objectif :

```text
ouvrir l’UI
```

---

# 55. Mini-lab 2 — datasource YAML

Créer :

```text
datasources/prometheus.yml
```

avec :

```text
Prometheus
```

comme datasource.

---

# 56. Mini-lab 3 — vérifier la datasource

Redémarrer Grafana.

Puis vérifier :

```text
datasource visible
```

---

# 57. Mini-lab 4 — premier dashboard

Créer dans l’UI :

```text
RNCP Bloc 3
```

Ajouter un panel basé sur une métrique réelle.

---

# 58. Mini-lab 5 — requêtes HTTP

Générer du trafic.

Observer :

```text
variation du panel
```

---

# 59. Mini-lab 6 — status codes

Générer :

```text
200
404
```

si les métriques permettent leur distinction.

Créer un panel par status.

---

# 60. Mini-lab 7 — méthode HTTP

Générer :

```text
GET
POST
```

si les labels permettent leur distinction.

Créer :

```text
Requests by Method
```

---

# 61. Mini-lab 8 — panne datasource

Changer volontairement :

```yaml
url: http://wrong-prometheus:9090
```

Observer l’échec.

Puis corriger.

---

# 62. Mini-lab 9 — PromQL incorrect

Utiliser un nom de métrique inexistant.

Observer :

```text
panel vide
```

Puis retrouver la vraie métrique depuis :

```text
/metrics
```

---

# 63. Mini-lab 10 — stack complète

Objectif :

```text
FastAPI
↓
Prometheus
↓
Grafana
```

avec :

```text
/health
/metrics
PromQL
dashboard
```

---

# 64. Checklist de maîtrise Grafana

```text
[ ] démarrer Grafana
[ ] accéder à l’UI
[ ] créer datasource YAML
[ ] pointer vers Prometheus
[ ] vérifier datasource
[ ] créer dashboard via UI
[ ] créer panel
[ ] choisir Prometheus
[ ] écrire PromQL
[ ] visualiser données
[ ] diagnostiquer panel vide
```

---

# 65. Questions flash

1. Quel outil de visualisation est explicitement annoncé ?
2. Comment la datasource doit-elle être configurée selon le support ?
3. Quelle source de données est naturellement utilisée dans le Bloc 3 ?
4. Grafana collecte-t-il les métriques ?
5. Quel langage alimente les panels Prometheus ?
6. Pourquoi `localhost:9090` peut-il être faux dans Docker ?
7. Que faire si un panel est vide ?
8. Quelle séquence doit être validée avant de travailler sur Grafana ?
9. Le dashboard doit-il être créé en YAML selon le support ?
10. Quelle chaîne complète mène de FastAPI au dashboard ?

---

# 66. Réponses flash

```text
1. Grafana.
2. via datasources/<source_name>.yml.
3. Prometheus.
4. non, il visualise.
5. PromQL.
6. localhost désigne le container Grafana.
7. vérifier Prometheus, requête, labels, time range, trafic.
8. API → /metrics → Prometheus UP → PromQL OK.
9. non, le support demande la création du dashboard depuis l’UI.
10. FastAPI → metrics → Prometheus → PromQL → Grafana.
```

---

# 67. Cheatsheet 30 secondes

Datasource :

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

Compose :

```yaml
grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
  volumes:
    - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
  depends_on:
    - prometheus
```

Validation :

```text
Prometheus UP
↓
PromQL OK
↓
Grafana datasource OK
↓
Dashboard
↓
Panel
```

---

# 68. Fil rouge à retenir

```text
PROMETHEUS
   ↓
DATASOURCE
   ↓
PROMQL
   ↓
PANEL
   ↓
DASHBOARD
```

---

# 69. Architecture observabilité finale

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
Grafana datasource
   ↓
Grafana dashboard
```

---

# 70. Document suivant

```text
11_RNCP_38919_BLOC_3_TEMPLATE_PROJECT.md
```

Objectif :

> assembler l’ensemble du Bloc 3 dans un template de projet cohérent :
> FastAPI, Pydantic, Pytest, GitLab CI, Docker, DockerHub,
> Kubernetes, Prometheus et Grafana.
