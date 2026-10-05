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
    # TODO : appeler validate_dataframe(sample_df()) sans lever d'erreur.
    pytest.fail("TODO test_valid_dataframe")


def test_missing_column():
    # TODO : retirer une colonne requise et attendre une ValueError.
    pytest.fail("TODO test_missing_column")


def test_duplicate_delivery_id():
    # TODO : dupliquer delivery_id et attendre une ValueError.
    pytest.fail("TODO test_duplicate_delivery_id")
