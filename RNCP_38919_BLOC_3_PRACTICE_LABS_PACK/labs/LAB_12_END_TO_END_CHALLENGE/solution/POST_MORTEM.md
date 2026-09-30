# Post-Mortem d'Incident — Défi d'Intégration End-to-End

Document de synthèse d'incident rédigé suite à la simulation d'examen blanc ParcelPulse.

---

## 1. Métriques de la session

* **Temps total de réalisation :** 3 heures 25 minutes (sur les 4 heures allouées).
* **Temps passé en debugging :** 45 minutes.
* **Taux de briques opérationnelles :** 100% après remédiation.

---

## 2. Chronologie et première panne rencontrée

* **T+00:45 :** L'API fonctionne en test unitaire avec un mock, mais crashe au démarrage réel avec `uvicorn` :
  ```text
  AttributeError: Can't get attribute 'DemoRiskModel' on <module '__main__'>
  ```
* **T+01:10 :** Déploiement Kubernetes appliqué, mais les pods restent bloqués indéfiniment à l'état `ContainerCreating` ou le PVC reste en `Pending`.

---

## 3. Causes racines identifiées

### Incident A — Sérialisation joblib / pickle sous `__main__`
* **Mécanisme :** La classe du modèle avait été définie directement dans le script générateur `create_artifact.py`. Lors de la sérialisation avec `joblib.dump()`, Python a enregistré la classe comme appartenant au module `__main__`.
* **Conséquence :** Lorsque le serveur API (`app.main`) ou un test tente de charger l'artefact avec `joblib.load()`, `__main__` désigne désormais le script uvicorn/pytest et non plus le générateur. Python ne trouve pas la classe et lève une exception fatale.

### Incident B — Absence de `storageClassName` explicite sur le PV/PVC
* **Mécanisme :** Le cluster local utilise un provisionneur dynamique par défaut. En l'absence de `storageClassName: manual`, le PVC a tenté de solliciter une classe de stockage dynamique au lieu de s'associer au `PersistentVolume` local statique déjà créé.
* **Conséquence :** Le PVC est resté en `Pending`, interdisant le montage du volume sur le pod.

---

## 4. Diagnostic et commandes utilisées

Pour l'incident de modèle :
```bash
# Inspection de la stacktrace complète
uvicorn app.main:app --port 8000
# Détection de l'origine du type de classe
python -c "import joblib; m = joblib.load('models/model.joblib'); print(type(m))"
```

Pour l'incident Kubernetes :
```bash
# Diagnostic de l'état du PVC
kubectl describe pvc model-pvc -n parcelpulse
# Vérification des évènements du Pod
kubectl describe pod -l app=parcelpulse-api -n parcelpulse
```

---

## 5. Mesures correctives immédiates

1. **Isolation du modèle :** Création du module `app/demo_model.py` contenant la classe `DemoRiskModel`. Importation de cette classe dans `create_artifact.py` et régénération de l'artefact `models/model.joblib`.
2. **Alignement du StorageClass :** Ajout de `storageClassName: manual` dans les spécifications du `PV` et du `PVC`.
3. **Prévention des montages vides :** Ajout d'un `initContainers` dans le déploiement Kubernetes afin de garantir que l'artefact est toujours copié sur le volume partagé si le montage hôte est vide.

---

## 6. Automatismes à retenir pour le Jour J

1. **Toujours tester l'import d'un artefact joblib dans un shell Python vierge** avant de conteneuriser l'application.
2. **Spécifier systématiquement `storageClassName: manual`** dès qu'un couple PV statique / PVC est déclaré.
3. **Consulter immédiatement `kubectl describe`** dès qu'un pod n'atteint pas l'état `Running` en moins de 30 secondes.
