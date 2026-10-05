from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW_PATH = PROJECT_ROOT / "data" / "raw" / "deliveries.json"
DEFAULT_PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "deliveries_clean.csv"

REQUIRED_COLUMNS = {
    "delivery_id",
    "customer_id",
    "customer_city",
    "vehicle_type",
    "distance_km",
    "traffic_level",
    "weather",
    "delivery_minutes",
    "late_delivery",
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

    result = df.drop_duplicates(subset=["delivery_id"], keep="first").copy()

    for column in ["customer_city", "vehicle_type"]:
        result[column] = (
            result[column].astype("string").str.strip().str.lower()
        )

    for column in ["traffic_level", "weather"]:
        result[column] = (
            result[column]
            .astype("string")
            .str.strip()
            .str.lower()
            .fillna("unknown")
        )

    result["distance_km"] = pd.to_numeric(result["distance_km"], errors="coerce")
    median_distance = result["distance_km"].median()
    result["distance_km"] = result["distance_km"].fillna(median_distance)

    for column in ["delivery_id", "customer_id", "delivery_minutes", "late_delivery"]:
        result[column] = pd.to_numeric(result[column], errors="raise")

    if result["delivery_id"].isna().any():
        raise ValueError("Null delivery_id detected")

    if not result["delivery_id"].is_unique:
        raise ValueError("Duplicate delivery_id detected")

    if not result["late_delivery"].isin([0, 1]).all():
        raise ValueError("late_delivery must contain only 0 or 1")

    return result


def save_processed(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def main() -> None:
    raw_df = extract(DEFAULT_RAW_PATH)
    clean_df = transform(raw_df)
    save_processed(clean_df, DEFAULT_PROCESSED_PATH)
    print(f"{len(clean_df)} rows written to {DEFAULT_PROCESSED_PATH}")


if __name__ == "__main__":
    main()
