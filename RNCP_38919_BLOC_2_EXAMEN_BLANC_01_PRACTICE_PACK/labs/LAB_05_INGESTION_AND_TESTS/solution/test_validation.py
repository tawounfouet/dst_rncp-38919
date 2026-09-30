import pandas as pd
import pytest

from validation import validate_dataframe

def sample_df():
    return pd.DataFrame({
        "delivery_id": [1, 2],
        "customer_id": [10, 11],
        "customer_city": ["paris", "poissy"],
        "vehicle_type": ["bike", "car"],
        "distance_km": [4.0, 12.0],
        "traffic_level": ["high", "low"],
        "weather": ["rain", "clear"],
        "delivery_minutes": [35, 30],
        "late_delivery": [1, 0],
    })

def test_valid_dataframe():
    validate_dataframe(sample_df())

def test_missing_column():
    df = sample_df().drop(columns=["weather"])
    with pytest.raises(ValueError):
        validate_dataframe(df)

def test_duplicate_delivery_id():
    df = pd.concat([sample_df(), sample_df().iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError):
        validate_dataframe(df)
