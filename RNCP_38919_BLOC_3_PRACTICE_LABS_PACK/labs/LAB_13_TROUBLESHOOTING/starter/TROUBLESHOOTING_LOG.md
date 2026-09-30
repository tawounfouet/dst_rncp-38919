# Journal de Résolution d'Incidents — Troubleshooting Log

Utilisez ce modèle pour consigner chaque blocage rencontré lors de vos sessions d'entraînement ou pendant l'examen blanc.  
Consigner précisément les faits permet d'éviter de tourner en rond et structure votre réflexion sous stress.

---

## Modèle de Journal

| # | Composant | Symptôme / Erreur | Preuve (Commande ou Log) | Cause racine identifiée | Solution appliquée |
|---|---|---|---|---|---|
| **Ex. 1** | Modèle / Joblib | `AttributeError: Can't get attribute on __main__` | `uvicorn app.main:app` renvoie un traceback python | Définition de la classe dans `__main__` du script | Isolation dans `app/demo_model.py` et réimport |
| **Ex. 2** | Kubernetes | Le PVC reste en statut `Pending` | `kubectl describe pvc model-pvc` montre "no persistent volumes available" | Omission de `storageClassName: manual` | Ajout du champ dans les manifestes PV et PVC |
| **1** | | | | | |
| **2** | | | | | |
| **3** | | | | | |
| **4** | | | | | |
| **5** | | | | | |

---

## Conseils méthodologiques

1. **Ne tentez pas de modifications au hasard :** Obtenez d'abord la preuve formelle de l'erreur via les logs (`docker logs`, `kubectl describe`, `pytest -vv`).
2. **Isolez la couche défaillante :** Vérifiez si le problème se produit aussi en local direct (hors conteneur).
3. **Validez une modification à la fois :** Re-testez immédiatement après avoir appliqué un correctif.
