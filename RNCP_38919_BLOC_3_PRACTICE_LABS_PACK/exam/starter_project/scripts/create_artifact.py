import sys
from pathlib import Path

# Garantit que la racine du projet est dans sys.path quel que soit le CWD
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
