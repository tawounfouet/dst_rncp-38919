# Plan de Remédiation — Lot 1 : Starter Project & Simulation d'Examen
**Priorité :** P0 (Bloquante)  
**Périmètre :** [`exam/starter_project/`](../../exam/starter_project/), [`exam/sujet/`](../../exam/sujet/)  
**Objectif :** Éliminer les ruptures de flux au lancement de l'examen blanc et garantir une expérience candidat 100% fluide sur 4 heures.

---

## 1. Diagnostic des Problèmes Ciblés

1. **Absence du script de génération d'artefact :**  
   Dans [`exam/starter_project/START_HERE.md`](../../exam/starter_project/START_HERE.md#L20), la consigne `python scripts/create_artifact.py` provoque un `FileNotFoundError` immédiat car le fichier est absent du sous-dossier `scripts/`.
2. **Ambiguïté sur l'artefact pré-existant :**  
   Le fichier binaire `models/model.joblib` est déjà présent dans le squelette, ce qui crée une contradiction entre l'instruction de génération et l'état réel du dépôt.
3. **Absence de test de sanité initial :**  
   Le candidat n'a aucun moyen simple de vérifier que son environnement virtuel `.venv` est correctement configuré avant d'entamer l'implémentation.
4. **Disparité des commentaires guides :**  
   Certains fichiers (`.gitlab-ci.yml`, `k8s/deployment.yml`) n'indiquent pas clairement si le candidat doit viser un déploiement local (Minikube) ou distant (DockerHub/GitLab SaaS).

---

## 2. Feuille d'Actions Détaillées

### Action 1.1 : Rétablir `scripts/create_artifact.py` dans le Starter Project
* **Cible :** `exam/starter_project/scripts/create_artifact.py`
* **Description :** Cloner la version autonome validée depuis [`exam/correction/reference_project/scripts/create_artifact.py`](../../exam/correction/reference_project/scripts/create_artifact.py).
* **Code à injecter :**
  ```python
  import sys
  from pathlib import Path

  # Garantit la résolution du module app quel que soit le CWD
  PROJECT_ROOT = Path(__file__).resolve().parent.parent
  if str(PROJECT_ROOT) not in sys.path:
      sys.path.insert(0, str(PROJECT_ROOT))

  import joblib
  from app.demo_model import DemoRiskModel

  models_dir = PROJECT_ROOT / "models"
  models_dir.mkdir(parents=True, exist_ok=True)
  output_path = models_dir / "model.joblib"
  joblib.dump(DemoRiskModel(), output_path)
  print(f"Artifact created: {output_path}")
  ```

---

### Action 1.2 : Réécriture et Sécurisation de `START_HERE.md`
* **Cible :** [`exam/starter_project/START_HERE.md`](../../exam/starter_project/START_HERE.md)
* **Modifications à apporter :**
  1. Expliquer que `model.joblib` est déjà pré-généré, mais que la commande `python scripts/create_artifact.py` permet de le régénérer à la demande.
  2. Ajouter une commande de vérification de version Python (3.10+ recommandée).
  3. Préciser le rôle exact de chaque étape avec estimation du temps alloué (aligné sur les 4 heures).

* **Diff prévisionnel :**
  ```diff
  --- a/exam/starter_project/START_HERE.md
  +++ b/exam/starter_project/START_HERE.md
  @@ -15,7 +15,9 @@
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
        ```
  -* Générer le modèle initial avec `python scripts/create_artifact.py`.
  +* (Optionnel) Régénérer l'artefact initial si besoin :
  +  ```bash
  +  python scripts/create_artifact.py
  +  ```
  ```

---

### Action 1.3 : Ajout d'un Smoke Test Minimal Guide
* **Cible :** `exam/starter_project/scripts/smoke_test.sh`
* **Description :** Plutôt que de laisser un fichier totalement vide de 4 lignes avec `# TODO`, fournir la structure Bash avec des variables prêtes à l'emploi (`API_URL=${API_URL:-http://localhost:8000}`) et des `curl` commentés à décommenter au fur et à mesure que les endpoints sont codés.
* **Bénéfice :** Permet à l'étudiant de tester visuellement chaque étape sans perdre de temps sur la syntaxe Bash.

---

### Action 1.4 : Clarification des Commentaires dans les Manifests Kubernetes
* **Cible :** `exam/starter_project/k8s/`
* **Description :**
  * Dans `deployment.yml`, indiquer explicitement :
    ```yaml
    # LOCAL (Minikube / Docker Desktop) : image: parcelpulse-api:latest + imagePullPolicy: IfNotPresent
    # DOCKERHUB : image: <VOTRE_USER>/parcelpulse-api:latest
    ```
  * Dans `pv.yml` et `pvc.yml`, ajouter la consigne :
    ```yaml
    # IMPORTANT : Définir explicitement storageClassName: manual pour éviter le conflit avec la classe par défaut
    ```

---

## 3. Protocole de Recette et Validation

1. **Test d'exécution propre :**
   ```bash
   cd exam/starter_project
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python scripts/create_artifact.py
   # Vérifier que models/model.joblib est mis à jour sans erreur
   ```
2. **Test d'intégrité statique :**
   Exécuter `tools/validate_reference_project.py` et s'assurer que le starter ne déclenche pas d'erreurs de syntaxe.
