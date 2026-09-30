from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "delivery_id", "customer_id", "customer_city",
    "vehicle_type", "distance_km", "traffic_level",
    "weather", "delivery_minutes", "late_delivery",
}

def extract(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_json(path)

def validate_schema(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

def transform(df: pd.DataFrame) -> pd.DataFrame:
    validate_schema(df)
    result = df.copy()
    result = result.drop_duplicates(subset=["delivery_id"], keep="first").copy()

    for col in ["customer_city", "vehicle_type"]:
        result[col] = result[col].astype("string").str.strip().str.lower()

    for col in ["traffic_level", "weather"]:
        result[col] = (
            result[col]
            .astype("string")
            .str.strip()
            .str.lower()
            .fillna("unknown")
        )

    result["distance_km"] = pd.to_numeric(result["distance_km"], errors="coerce")
    result["distance_km"] = result["distance_km"].fillna(result["distance_km"].median())

    if not result["delivery_id"].is_unique:
        raise ValueError("Duplicate delivery_id detected")

    return result

def save_processed(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
