from pathlib import Path
import pandas as pd

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
    # TODO
    raise NotImplementedError

def validate_schema(df: pd.DataFrame) -> None:
    # TODO
    raise NotImplementedError

def transform(df: pd.DataFrame) -> pd.DataFrame:
    # TODO
    raise NotImplementedError

def save_processed(df: pd.DataFrame, path: str | Path) -> None:
    # TODO
    raise NotImplementedError
