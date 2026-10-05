import pandas as pd
import pytest

from src.etl import extract, transform, validate_schema


def valid_df() -> pd.DataFrame:
    return pd.DataFrame({
        "delivery_id": [1, 2],
        "customer_id": [10, 11],
        "customer_city": [" Paris ", "POISSY"],
        "vehicle_type": ["Bike", "Car"],
        "distance_km": [5.0, 10.0],
        "traffic_level": ["High", "Low"],
        "weather": ["Rain", "Clear"],
        "delivery_minutes": [30, 25],
        "late_delivery": [1, 0],
    })


def test_valid_schema():
    validate_schema(valid_df())


def test_missing_column_is_rejected():
    df = valid_df().drop(columns=["weather"])
    with pytest.raises(ValueError):
        validate_schema(df)


def test_duplicate_delivery_is_removed():
    df = valid_df()
    duplicate = df.iloc[[0]].copy()
    df = pd.concat([df, duplicate], ignore_index=True)

    result = transform(df)

    assert result["delivery_id"].is_unique
    assert len(result) == 2


def test_city_is_normalized():
    result = transform(valid_df())
    assert result.loc[0, "customer_city"] == "paris"
    assert result.loc[1, "customer_city"] == "poissy"


def test_missing_distance_is_imputed():
    df = valid_df()
    df.loc[0, "distance_km"] = None

    result = transform(df)

    assert not result["distance_km"].isna().any()


def test_missing_file_is_an_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract(tmp_path / "missing.json")
