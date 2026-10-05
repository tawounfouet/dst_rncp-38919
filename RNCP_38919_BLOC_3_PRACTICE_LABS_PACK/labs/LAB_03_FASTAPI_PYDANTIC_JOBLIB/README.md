# LAB 03 — FastAPI, Pydantic et Joblib

## Objectifs pédagogiques

- Créer une API REST moderne haute performance avec **FastAPI** ;
- Valider et typer strictement les requêtes entrantes avec **Pydantic** (`BaseModel`) ;
- Charger et exploiter un modèle de Machine Learning sérialisé avec **Joblib** ;
- Instrumenter l'API pour exposer des métriques de supervision Prometheus (`/metrics`).

---

## Architecture de l'API FastAPI

```mermaid
graph TD
    Client["Client HTTP (curl / urllib / browser)"]
    
    subgraph API ["FastAPI Application (:8000)"]
        Router["Endpoints Routeur"]
        Health["GET /health"]
        Predict["POST /predict"]
        Metrics["GET /metrics"]
        
        Pydantic["Validation Pydantic (Payload)"]
        JoblibModel["Modèle ML (model.joblib)"]
        Prometheus["Instrumentator Prometheus"]
    end
    
    Client -->|GET /health| Health
    Client -->|POST /predict + JSON| Predict
    Client -->|GET /metrics| Metrics
    
    Predict --> Pydantic
    Pydantic -->|distance_km, package_weight_kg| JoblibModel
    JoblibModel -->|{"risk": 0 ou 1}| Client
    Metrics --> Prometheus
```

### Schéma ASCII équivalent

```text
+-----------------------------------------------------------------------------------+
|               ARCHITECTURE DE L'APPLICATION FASTAPI (LAB 03)                      |
+-----------------------------------------------------------------------------------+

     [Client HTTP : curl / testeur / browser]
            │
            ├──► GET  /health   ────────► Statut de santé : {"status": "ok"}
            │
            ├──► POST /predict  ────────► 1. Validation Pydantic (champs typés float)
            │    (JSON payload)           2. Inférence Joblib : model.predict([[...]])
            │                             3. Réponse JSON : {"risk": 0 ou 1}
            │
            └──► GET  /metrics  ────────► Scraping Prometheus (temps de réponse, RPS, ...)
```

---

## 1. Pré-requis : Environnement Virtuel & Dépendances

Ce lab utilise des bibliothèques externes (`fastapi`, `uvicorn`, `pydantic`, `joblib`, `prometheus-fastapi-instrumentator`). Il est fortement recommandé d'utiliser un environnement virtuel isolé :

### Création et activation de l'environnement virtuel

```bash
# 1. Se placer à la racine du LAB 03
cd labs/LAB_03_FASTAPI_PYDANTIC_JOBLIB

# 2. Créer l'environnement virtuel .venv
python3 -m venv .venv

# 3. Activer l'environnement virtuel
source .venv/bin/activate
# (Sur Windows Git Bash : source .venv/Scripts/activate)

# 4. Installer les dépendances
pip install -r requirements.txt
pip install --no-user -r requirements.txt
# Note : L'option --no-user désactive l'installation utilisateur si PIP_USER=true est défini sur votre Mac.
```

Le fichier [`requirements.txt`](requirements.txt) contient :
- `fastapi` : Framework web asynchrone
- `uvicorn` : Serveur ASGI léger
- `pydantic` : Validation et parsing de données
- `joblib` : Chargement du modèle ML
- `prometheus-fastapi-instrumentator` : Export automatique des métriques Prometheus
- `httpx` : Client HTTP pour les tests

---

## 2. Lancement du Serveur Uvicorn

> [!TIP]
> **Bonne pratique recommandée :** Utilisez toujours `python -m uvicorn` au lieu de `uvicorn` seul. Si vous avez Conda activé en arrière-plan (`(base)`), taper `uvicorn` risque d'appeler `/opt/miniconda3/bin/uvicorn` au lieu du Uvicorn de votre `.venv` !

Attention au **répertoire courant** (`pwd`) lors de l'exécution :

### Cas A : Vous êtes à la racine de `labs/LAB_03_FASTAPI_PYDANTIC_JOBLIB`
```bash
# Pour lancer la solution avec le Python du venv :
python -m uvicorn solution.app:app --host 0.0.0.0 --port 8000 --reload

# (Ou via le binaire direct du venv : .venv/bin/uvicorn solution.app:app --port 8000 --reload)

# Pour lancer votre starter en cours de développement :
python -m uvicorn starter.app:app --host 0.0.0.0 --port 8000 --reload
```

### Cas B : Vous êtes dans le sous-dossier `solution/`
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

---

## 3. Guide de Dépannage & Erreurs Fréquentes

### Erreur 1 : `ModuleNotFoundError: No module named 'solution'`
* **Contexte :** Vous avez tapé `uvicorn solution.app:app` alors que votre terminal se trouve déjà dans le sous-dossier `solution/`.
* **Explication :** Python cherche un dossier `solution` à l'intérieur de `solution/`, qui n'existe pas.
* **Solution :** Si vous êtes dans `solution/`, tapez simplement `python -m uvicorn app:app --port 8000`.

### Erreur 2 : `ModuleNotFoundError: No module named 'prometheus_fastapi_instrumentator'`
* **Contexte :** Vous avez lancé Uvicorn avec le Python global ou Conda sans activer le venv du lab.
* **Explication :** La bibliothèque de métriques Prometheus n'est pas installée dans votre environnement actif.
* **Solution :** 
  1. Activez le venv : `source .venv/bin/activate` ;
  2. Installez les packages : `pip install --no-user -r requirements.txt`.
  *(Note : Le code intègre un fallback gracieux qui permet à l'API de démarrer même si ce package est absent).*

### Erreur 3 : `ERROR: Can not perform a '--user' install. User site-packages are not visible in this virtualenv.`
* **Contexte :** Lors de l'exécution de `pip install -r requirements.txt` dans un venv actif.
* **Explication :** La variable d'environnement `PIP_USER=true` ou une option globale dans `~/.pip/pip.conf` force pip à installer les paquets dans le répertoire utilisateur personnel (`--user`). Or, Python interdit les installations `--user` dans un environnement virtuel afin de garantir son étanchéité.
* **Solution :** Spécifiez le drapeau `--no-user` :
  ```bash
  pip install --no-user -r requirements.txt
  ```
  *Ou préfixez la commande par : `PIP_USER=0 pip install -r requirements.txt`.*

### Erreur 4 : `ModuleNotFoundError: No module named 'joblib'` malgré une installation réussie
* **Contexte :** Après avoir exécuté avec succès `pip install --no-user -r requirements.txt`, la commande `uvicorn solution.app:app` échoue sur `import joblib`.
* **Explication :** Regardez attentivement la trace d'erreur :
  `File "/opt/miniconda3/bin/uvicorn", line 6, in <module>`
  La commande `uvicorn` a appelé le binaire global de Miniconda (qui utilise Python Conda, où `joblib` n'est pas installé) au lieu de celui de votre `.venv` !
* **Solution :** Lancez Uvicorn via l'interpréteur du venv actif :
  ```bash
  python -m uvicorn solution.app:app --host 0.0.0.0 --port 8000 --reload
  ```
  *Ou directement : `.venv/bin/uvicorn solution.app:app --host 0.0.0.0 --port 8000 --reload`.*

---

## 4. Tests des Endpoints avec cURL

Dans un **second terminal**, testez les trois endpoints de l'API :

### 1. Test GET `/health`
```bash
curl -i http://localhost:8000/health
```
*Sortie attendue : `HTTP/1.1 200 OK` avec `{"status":"ok"}`.*

### 2. Test POST `/predict` (Inférence)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"distance_km": 12.5, "package_weight_kg": 3.2}'
```
*Sortie attendue : `{"risk": 0}` ou `{"risk": 1}` selon les valeurs d'entrée.*

### 3. Test de validation Pydantic (Erreur 422 si données invalides)
Envoyez un champ manquant ou de mauvais type :
```bash
curl -i -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"distance_km": "non_numerique"}'
```
*Sortie attendue : `HTTP/1.1 422 Unprocessable Entity` détaillant l'erreur de validation.*

### 4. Test GET `/metrics` (Supervision Prometheus)
```bash
curl -i http://localhost:8000/metrics
```
*Sortie attendue : Métriques Prometheus au format OpenMetrics textuel (`http_requests_total`, `http_request_duration_seconds_bucket`, etc.).*

---

## Structure du Lab

```text
labs/LAB_03_FASTAPI_PYDANTIC_JOBLIB/
├── README.md               # Guide complet, résolution des erreurs et commandes
├── requirements.txt        # Dépendances requises (FastAPI, Uvicorn, Prometheus, ...)
├── starter/
│   └── app.py              # Squelette de code à implémenter
└── solution/
    └── app.py              # Solution complète et résiliente avec fallback
```
