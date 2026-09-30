from pathlib import Path
import joblib


def load_model(path: str):
    model_path = Path(path)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at '{model_path}'. "
            "Please generate it by running: python scripts/create_artifact.py"
        )
    return joblib.load(model_path)

