import pandas as pd
import pytest
from sqlalchemy import create_engine

from ingest import count_rows, ingest


@pytest.fixture
def engine(tmp_path):
    return create_engine(f"sqlite:///{tmp_path / 'deliveries.sqlite'}")


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


def test_first_ingestion_inserts_all(engine):
    assert ingest(sample_df(), engine) == 2
    assert count_rows(engine) == 2


def test_reingestion_does_not_duplicate(engine):
    ingest(sample_df(), engine)
    assert ingest(sample_df(), engine) == 0
    assert count_rows(engine) == 2


def test_partial_reingestion_inserts_only_new(engine):
    ingest(sample_df(), engine)
    extended = pd.concat([sample_df(), sample_df().iloc[[0]].assign(delivery_id=3)],
                         ignore_index=True)
    assert ingest(extended, engine) == 1
    assert count_rows(engine) == 3


def test_ingest_rejects_invalid_dataframe(engine):
    invalid = sample_df().drop(columns=["weather"])
    with pytest.raises(ValueError):
        ingest(invalid, engine)
