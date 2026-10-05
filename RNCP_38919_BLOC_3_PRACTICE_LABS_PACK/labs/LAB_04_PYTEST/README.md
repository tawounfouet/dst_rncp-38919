# LAB 04 — Pytest

Écrire les tests suivants :

```text
health 200
predict valide 200
predict invalide != 200
metrics 200
```

Puis intégrer `pytest -v` dans une étape CI de practice.

## Exécution des tests

Pour lancer les tests de la solution avec résolution de l'application :
```bash
# Option 1 : Depuis la solution du reference_project (contexte complet)
cd ../../exam/correction/reference_project
pytest -v

# Option 2 : Depuis ce dossier en injectant le PYTHONPATH
PYTHONPATH=../../exam/correction/reference_project pytest -v solution/test_api.py
```
