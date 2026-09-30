# DataScientest — Certification RNCP 38919 (Data Engineer)

Ce dépôt regroupe les packs d'entraînement, ressources de cadrage, projets de référence et documentations techniques pour la préparation aux examens de la certification professionnelle **RNCP 38919 — Data Engineer**.

---

## 📚 Sommaire du Répertoire

```text
RNCP/
├── Consignes surveillance évaluation.pdf    # Cadre officiel d'évaluation
├── Examen RNCP 38919 _ Bloc 2 - ORM.pdf     # Sujet de référence Bloc 2 (ORM)
├── Examen RNCP 38919 _ Bloc 2 - Projet ETL & ML.pdf # Cadrage Bloc 2 (ETL & ML)
│
├── RNCP_38919_BLOC_2_EXAMEN_BLANC_01_PRACTICE_PACK/
│   ├── 00_GUIDE_UTILISATION_PACK.md
│   ├── exam/                               # Sujet blanc et correction Bloc 2
│   ├── labs/                               # Labs pratiques pas-à-pas (SQL, ORM, ETL)
│   └── resources/                          # Données brutes et artefacts
│
└── RNCP_38919_BLOC_3_PRACTICE_LABS_PACK/
    ├── README.md
    ├── START_HERE.md
    ├── VALIDATION_REPORT.txt               # Statut de validation 100% opérationnel
    ├── docs/                               # Suite d'audit, remédiation et REX
    │   ├── AUDIT_ET_ANALYSE_OPERATIONNELLE_CORRECTION.md
    │   ├── PLAN_IMPLEMENTATION_CORRECTIFS_ET_AMELIORATIONS.md
    │   └── FEEDBACK_ET_RETOUR_EXPERIENCE.md
    ├── exam/
    │   ├── sujet/                          # Énoncé officiel examen blanc (ParcelPulse)
    │   ├── starter_project/                # Projet d'entraînement (TODOs candidat)
    │   └── correction/                     # Corrigé détaillé et Reference Project
    │       ├── 15_RNCP_38919_BLOC_3_CORRIGE_EXAMEN_BLANC_01.md
    │       └── reference_project/          # Solution 100% opérationnelle
    ├── labs/                               # 13 labs pratiques (Bash, Docker, K8s, etc.)
    └── tools/                              # Scripts de validation automatisée
```

---

## 🎯 Blocs de Compétences Couverts

### 1. Bloc 2 — Conception et Développement d'Infrastructures de Données
- Modélisation relationnelle et ORM (SQLAlchemy, PostgreSQL).
- Pipelines d'ingestion et transformation ETL.
- Entraînement et sérialisation d'artefacts Machine Learning.

### 2. Bloc 3 — Industrialisation et Déploiement d'un Modèle d'IA et de son API
- **Examen Blanc 01 (ParcelPulse)** :
  - **API REST** : FastAPI + validation stricte avec Pydantic v2.
  - **Machine Learning** : Sérialisation et chargement robuste avec `joblib`.
  - **Tests** : Suite Pytest unitaire et d'intégration + scripts de smoke test.
  - **Containerisation** : Dockerfile multi-couche + orchestration Docker Compose (API + Prometheus + Grafana).
  - **Orchestration Kubernetes** : Namespace, ConfigMap, PersistentVolume (hostPath/manual), PersistentVolumeClaim, Deployment (avec `initContainers`), Service.
  - **Observabilité** : Métriques via `prometheus-fastapi-instrumentator`, scraping Prometheus et dashboards Grafana.
  - **CI/CD** : Pipeline GitLab CI automatisé compatible avec runners Docker (dind) et Shell.

---

## 🧪 Validation & Contrôle Qualité

Le projet de référence du Bloc 3 a été intégralement audité, remédié et certifié opérationnel à 100% :

```bash
# Vérification end-to-end de la solution de référence :
python RNCP_38919_BLOC_3_PRACTICE_LABS_PACK/tools/validate_reference_project.py

# Exécution des tests unitaires :
cd RNCP_38919_BLOC_3_PRACTICE_LABS_PACK/exam/correction/reference_project
pytest -v
```

Pour plus de détails sur les analyses techniques et les bonnes pratiques :
- Consulter le [Guide de Feedback & REX](./RNCP_38919_BLOC_3_PRACTICE_LABS_PACK/docs/FEEDBACK_ET_RETOUR_EXPERIENCE.md)
- Consulter l'[Audit Technique](./RNCP_38919_BLOC_3_PRACTICE_LABS_PACK/docs/AUDIT_ET_ANALYSE_OPERATIONNELLE_CORRECTION.md)
- Consulter le [Plan d'Implémentation](./RNCP_38919_BLOC_3_PRACTICE_LABS_PACK/docs/PLAN_IMPLEMENTATION_CORRECTIFS_ET_AMELIORATIONS.md)
