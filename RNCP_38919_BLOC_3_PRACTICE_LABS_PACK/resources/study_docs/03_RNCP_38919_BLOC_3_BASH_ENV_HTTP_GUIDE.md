# 03 — RNCP 38919 — Bloc 3
# Guide Bash, variables d’environnement, HTTP et joblib

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Convention**
>
> - **Attendu source** : notion explicitement annoncée dans le support DataScientest.
> - **Guide pratique** : exemples, commandes et mini-labs proposés pour réviser.
>
> Le support annonce explicitement :
>
> ```text
> export
> .bashrc
> variables d’environnement dans Python
> environnements virtuels Python
> requêtes HTTP via Bash
> requêtes HTTP via Python
> curl
> joblib
> ```
>
> Il ne fixe pas, dans la page fournie, une bibliothèque Python HTTP précise ni une structure de projet imposée.

---

# 1. Objectif de ce guide

Cette partie couvre les fondamentaux système et Python qui servent de base à tout le Bloc 3.

Modèle mental :

```text
Shell
  ↓
Variables d’environnement
  ↓
Python
  ↓
HTTP
  ↓
Artefacts joblib
```

Ces notions réapparaissent ensuite dans :

```text
FastAPI
GitLab CI
Docker
Kubernetes
Prometheus
```

---

# 2. `export` — variable d’environnement dans Bash

## Attendu source

Le support demande de savoir initialiser des variables via :

```bash
export
```

## Guide pratique

Créer :

```bash
export API_URL=http://localhost:8000
```

Lire :

```bash
echo $API_URL
```

Vérifier dans l’environnement :

```bash
env | grep API_URL
```

---

# 3. Durée de vie d’une variable `export`

## Guide pratique

Une variable exportée dans un terminal est disponible :

```text
dans le shell courant
et dans les processus enfants
```

Exemple :

```bash
export APP_ENV=development
python app.py
```

Le script Python peut alors lire :

```python
os.getenv("APP_ENV")
```

---

# 4. Variable locale vs variable exportée

## Guide pratique

Variable shell simple :

```bash
APP_ENV=development
```

Variable exportée :

```bash
export APP_ENV=development
```

Différence mentale :

```text
VAR=value
→ connue du shell

export VAR=value
→ propagée aux processus enfants
```

---

# 5. `.bashrc`

## Attendu source

Le support demande de savoir modifier :

```text
le shell Bash via le fichier .bashrc
```

## Guide pratique

Ajouter une variable :

```bash
echo 'export API_URL=http://localhost:8000' >> ~/.bashrc
```

Recharger :

```bash
source ~/.bashrc
```

Vérifier :

```bash
echo $API_URL
```

---

# 6. Lire `.bashrc`

```bash
cat ~/.bashrc
```

ou :

```bash
less ~/.bashrc
```

Rechercher une variable :

```bash
grep API_URL ~/.bashrc
```

---

# 7. Modifier proprement `.bashrc`

## Guide pratique

Avec un éditeur :

```bash
nano ~/.bashrc
```

ou :

```bash
vim ~/.bashrc
```

Puis :

```bash
source ~/.bashrc
```

---

# 8. Piège — doublonner des exports

Éviter :

```text
export API_URL=...
export API_URL=...
export API_URL=...
```

dans `.bashrc`.

Vérifier avant :

```bash
grep API_URL ~/.bashrc
```

---

# 9. Supprimer une variable

Session courante :

```bash
unset API_URL
```

Puis :

```bash
echo $API_URL
```

doit être vide.

---

# 10. Variables d’environnement dans Python

## Attendu source

Le support demande :

```text
l'utilisation de variables d'environnement
dans des scripts Python
```

## Guide pratique

```python
import os

api_url = os.getenv(
    "API_URL"
)
```

---

# 11. Valeur par défaut

```python
api_url = os.getenv(
    "API_URL",
    "http://localhost:8000",
)
```

---

# 12. Vérifier qu’une variable obligatoire existe

```python
import os

api_url = os.getenv(
    "API_URL"
)

if api_url is None:
    raise RuntimeError(
        "API_URL is required"
    )
```

---

# 13. `os.environ`

Alternative :

```python
import os

api_url = os.environ[
    "API_URL"
]
```

Différence pratique :

```text
os.getenv(...)
→ None / défaut si absente

os.environ["VAR"]
→ erreur si absente
```

---

# 14. Chaîne complète Shell → Python

```text
export API_URL=...
        ↓
environnement shell
        ↓
python app.py
        ↓
os.getenv("API_URL")
```

---

# 15. Variables utiles pour les labs Bloc 3

## Guide pratique

Exemple :

```bash
export API_HOST=0.0.0.0
export API_PORT=8000
export MODEL_PATH=models/model.joblib
export PROMETHEUS_URL=http://localhost:9090
```

Puis en Python :

```python
import os

model_path = os.getenv(
    "MODEL_PATH",
    "models/model.joblib",
)
```

---

# 16. Environnement virtuel Python

## Attendu source

Le support cite :

```text
l'initialisation d'environnements virtuels
pour des projets Python
```

## Guide pratique

Créer :

```bash
python -m venv .venv
```

Activer :

```bash
source .venv/bin/activate
```

---

# 17. Vérifier le Python actif

```bash
which python
```

Puis :

```bash
python --version
```

Dans un venv correctement activé, le chemin doit pointer vers :

```text
.venv/
```

---

# 18. Installer des dépendances

```bash
pip install \
  fastapi \
  uvicorn \
  pytest \
  joblib
```

---

# 19. `requirements.txt`

Enregistrer :

```bash
pip freeze > requirements.txt
```

Réinstaller :

```bash
pip install \
  -r requirements.txt
```

---

# 20. Désactiver le venv

```bash
deactivate
```

---

# 21. Recréer un environnement

Pattern :

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

À retenir pour :

```text
local
CI
Docker
```

---

# 22. HTTP — concepts à connaître

## Attendu source

Le support demande des requêtes :

```text
avec Bash
et
avec Python
```

## Guide pratique

Toujours identifier :

```text
method
URL
headers
body
status code
response body
```

---

# 23. `curl` — GET

## Attendu source

Le support cite explicitement :

```text
curl
```

## Guide pratique

```bash
curl \
  http://localhost:8000/
```

---

# 24. `curl` — afficher headers

```bash
curl \
  -i \
  http://localhost:8000/
```

---

# 25. `curl` — verbose

```bash
curl \
  -v \
  http://localhost:8000/
```

Utile pour :

```text
connexion
DNS
headers
status
```

---

# 26. `curl` — POST JSON

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"value": 42}' \
  http://localhost:8000/predict
```

---

# 27. `curl` — variables Bash

```bash
export API_URL=http://localhost:8000
```

Puis :

```bash
curl \
  "$API_URL/health"
```

---

# 28. `curl` — Authorization header

Pattern de pratique :

```bash
curl \
  -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/private
```

> Le support fourni n’annonce pas explicitement un mécanisme d’authentification ; cet exemple sert uniquement à pratiquer les headers.

---

# 29. Codes HTTP à reconnaître

## Guide pratique

```text
200 OK
201 Created
400 Bad Request
404 Not Found
422 Validation Error
500 Internal Server Error
```

Dans FastAPI, un payload invalide peut notamment conduire à :

```text
422
```

---

# 30. Requêtes HTTP en Python

## Attendu source

Le support annonce :

```text
Python
→ requêtes vers une URL
```

mais ne précise pas de bibliothèque.

## Guide pratique

Exemple avec `urllib`, inclus dans Python :

```python
from urllib.request import (
    urlopen,
)

with urlopen(
    "http://localhost:8000/"
) as response:
    body = response.read()

print(body)
```

---

# 31. Requête Python avec données JSON

## Guide pratique

Exemple standard-library :

```python
import json
from urllib.request import (
    Request,
    urlopen,
)


payload = {
    "value": 42
}


request = Request(
    "http://localhost:8000/predict",
    data=json.dumps(
        payload
    ).encode(
        "utf-8"
    ),
    headers={
        "Content-Type":
        "application/json"
    },
    method="POST",
)


with urlopen(
    request
) as response:
    result = json.loads(
        response.read()
    )


print(result)
```

---

# 32. Lire le status code en Python

```python
with urlopen(
    "http://localhost:8000/"
) as response:
    print(
        response.status
    )
```

---

# 33. Gérer une erreur HTTP

## Guide pratique

```python
from urllib.error import (
    HTTPError,
    URLError,
)
```

Pattern :

```python
try:
    ...
except HTTPError as exc:
    print(
        exc.code
    )
except URLError as exc:
    print(
        exc.reason
    )
```

---

# 34. Bash HTTP vs Python HTTP

```text
curl
→ test rapide manuel

Python
→ intégration dans un script
```

Le Bloc 3 demande explicitement les deux approches.

---

# 35. `joblib` — sauvegarde

## Attendu source

Le support cite `joblib` pour enregistrer :

```text
modèles ML
et autres objets liés à la data science
```

## Guide pratique

```python
import joblib

joblib.dump(
    model,
    "model.joblib",
)
```

---

# 36. `joblib` — chargement

```python
model = joblib.load(
    "model.joblib"
)
```

---

# 37. Vérifier le fichier

```python
from pathlib import Path

model_path = Path(
    "model.joblib"
)

print(
    model_path.exists()
)
```

---

# 38. Créer le dossier d’artefacts

```python
from pathlib import Path

Path(
    "models"
).mkdir(
    parents=True,
    exist_ok=True,
)
```

Puis :

```python
joblib.dump(
    model,
    "models/model.joblib",
)
```

---

# 39. Pattern variable d’environnement + joblib

```bash
export MODEL_PATH=models/model.joblib
```

Python :

```python
import os
import joblib

model_path = os.getenv(
    "MODEL_PATH",
    "models/model.joblib",
)

model = joblib.load(
    model_path
)
```

Chaîne :

```text
Shell config
↓
Python env var
↓
joblib.load
```

---

# 40. Cas FastAPI + joblib

## Guide pratique

Pattern conceptuel :

```text
startup
↓
joblib.load
↓
FastAPI
↓
POST /predict
↓
model.predict
```

Exemple :

```python
import os
import joblib

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "models/model.joblib",
)


model = joblib.load(
    MODEL_PATH
)


class Payload(
    BaseModel
):
    value: float


@app.post("/predict")
def predict(
    payload: Payload,
):
    prediction = model.predict(
        [[payload.value]]
    )

    return {
        "prediction":
        prediction[0]
    }
```

> Cet exemple est un pattern de préparation. Le support n’impose pas cet endpoint précis.

---

# 41. Vérifier une API avec `curl`

Health :

```bash
curl \
  http://localhost:8000/health
```

Predict :

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"value": 42}' \
  http://localhost:8000/predict
```

---

# 42. Vérifier la configuration avant lancement

```bash
echo $MODEL_PATH
echo $API_PORT
```

Puis :

```bash
python app.py
```

---

# 43. Pièges fréquents — env vars

```text
variable non exportée
faute de frappe dans le nom
.bashrc modifié mais non rechargé
variable présente dans un terminal mais pas un autre
```

---

# 44. Pièges fréquents — venv

```text
venv non activé
pip global utilisé
requirements incomplet
mauvais Python
```

Vérifier :

```bash
which python
which pip
```

---

# 45. Pièges fréquents — HTTP

```text
mauvais port
mauvaise URL
mauvaise méthode
Content-Type absent
JSON invalide
service non démarré
```

---

# 46. Pièges fréquents — `curl`

À vérifier :

```text
guillemets
échappement JSON
-X POST
-H Content-Type
-d payload
```

---

# 47. Pièges fréquents — `joblib`

```text
fichier absent
mauvais chemin
dossier absent
objet incompatible
artefact produit avec une version différente
```

---

# 48. Debug Bash

```bash
echo $VAR
env | grep VAR
grep VAR ~/.bashrc
```

---

# 49. Debug Python env

```python
import os

print(
    os.environ
)
```

Ou ciblé :

```python
print(
    os.getenv(
        "API_URL"
    )
)
```

---

# 50. Debug HTTP avec `curl`

```bash
curl \
  -v \
  http://localhost:8000/health
```

---

# 51. Debug port local

Pattern Linux :

```bash
ss -ltn
```

ou :

```bash
ss -ltnp
```

> Ces commandes ne sont pas mentionnées dans la page DataScientest ; elles sont ajoutées comme réflexes de diagnostic.

---

# 52. Mini-lab 1 — `export`

## Mission

Créer :

```text
APP_ENV=dev
API_PORT=8000
```

avec :

```bash
export
```

Puis vérifier :

```bash
echo $APP_ENV
echo $API_PORT
```

---

# 53. Mini-lab 2 — `.bashrc`

Ajouter :

```text
APP_NAME=bloc3-practice
```

dans `.bashrc`.

Fermer puis rouvrir un shell ou exécuter :

```bash
source ~/.bashrc
```

Vérifier :

```bash
echo $APP_NAME
```

---

# 54. Mini-lab 3 — Python env vars

Créer :

```text
env_demo.py
```

avec :

```python
import os

print(
    os.getenv(
        "APP_NAME"
    )
)
```

Puis :

```bash
python env_demo.py
```

---

# 55. Mini-lab 4 — environnement virtuel

Créer :

```text
.venv
```

Installer :

```text
joblib
pytest
```

Puis produire :

```text
requirements.txt
```

---

# 56. Mini-lab 5 — HTTP avec `curl`

Si une API locale répond sur :

```text
localhost:8000
```

tester :

```bash
curl \
  http://localhost:8000/health
```

Puis :

```bash
curl \
  -i \
  http://localhost:8000/health
```

---

# 57. Mini-lab 6 — HTTP Python

Créer un script :

```text
client.py
```

qui :

```text
1. lit API_URL depuis l’environnement
2. fait un GET
3. affiche le status
4. affiche le body
```

---

# 58. Mini-lab 7 — joblib

Créer un objet Python simple :

```python
artifact = {
    "name": "bloc3",
    "version": 1,
}
```

Sauvegarder :

```python
joblib.dump(
    artifact,
    "artifact.joblib",
)
```

Puis le recharger et vérifier :

```python
assert (
    loaded["name"]
    == "bloc3"
)
```

---

# 59. Mini-lab 8 — env + joblib

Définir :

```bash
export ARTIFACT_PATH=artifacts/demo.joblib
```

Le script doit :

```text
lire ARTIFACT_PATH
créer le dossier
sauvegarder
recharger
afficher
```

---

# 60. Mini-lab 9 — mini chaîne HTTP

Construire :

```text
Shell
↓
API_URL
↓
client Python
↓
GET /health
```

Puis comparer le résultat avec :

```bash
curl
```

---

# 61. Checkpoint de maîtrise

Être capable sans aide de reconstruire :

```bash
export API_URL=http://localhost:8000
source ~/.bashrc
python -m venv .venv
source .venv/bin/activate
curl http://localhost:8000/health
```

et en Python :

```python
os.getenv(...)
joblib.dump(...)
joblib.load(...)
```

---

# 62. Questions flash

1. À quoi sert `export` ?
2. À quoi sert `.bashrc` ?
3. Pourquoi `source ~/.bashrc` ?
4. Différence entre `os.getenv` et `os.environ["VAR"]` ?
5. Comment créer un venv ?
6. Comment activer un venv ?
7. Comment faire un GET avec `curl` ?
8. Comment faire un POST JSON avec `curl` ?
9. Quels éléments d’une requête HTTP faut-il reconnaître ?
10. À quoi sert `joblib.dump` ?
11. À quoi sert `joblib.load` ?
12. Pourquoi mettre le chemin du modèle dans une variable d’environnement ?

---

# 63. Réponses flash

```text
1. exporter une variable vers les processus enfants.
2. configurer Bash lors du démarrage du shell interactif.
3. recharger immédiatement les modifications.
4. getenv peut retourner None/défaut ; environ[...] lève une erreur si absente.
5. python -m venv .venv.
6. source .venv/bin/activate.
7. curl URL.
8. curl -X POST -H ... -d ...
9. method, URL, headers, body, status, response.
10. sérialiser un objet vers un fichier.
11. recharger l’objet.
12. séparer la configuration du code.
```

---

# 64. Cheatsheet 30 secondes

```bash
export VAR=value
echo $VAR

source ~/.bashrc

python -m venv .venv
source .venv/bin/activate

curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"value": 1}' \
  http://localhost:8000/predict
```

Python :

```python
import os
import joblib

value = os.getenv(
    "VAR"
)

joblib.dump(
    obj,
    "obj.joblib",
)

obj = joblib.load(
    "obj.joblib"
)
```

---

# 65. Fil rouge à retenir

```text
CONFIG
  ↓
SHELL
  ↓
PYTHON
  ↓
HTTP
  ↓
ARTEFACT
```

Cette base sera ensuite utilisée dans :

```text
FastAPI
GitLab CI
Docker
Kubernetes
```

---

# 66. Document suivant

```text
04_RNCP_38919_BLOC_3_GITLAB_CICD_RUNNER_GUIDE.md
```

Objectif :

> approfondir la partie GitLab explicitement annoncée dans le support :
> repository, `.gitlab-ci.yml`, pipeline, Runner `shell`, SSH et préparation de la CI/CD.
