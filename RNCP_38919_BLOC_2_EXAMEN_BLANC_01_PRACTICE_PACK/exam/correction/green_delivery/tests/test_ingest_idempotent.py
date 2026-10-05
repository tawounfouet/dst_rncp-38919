"""Test d'intégration : nécessite la base MariaDB démarrée (docker compose up -d).

Exécution :
    RUN_DB_TESTS=1 pytest -v tests/test_ingest_idempotent.py
"""

import os

import pandas as pd
import pytest

from src.database import Session
from src.etl import DEFAULT_PROCESSED_PATH
from src.ingest import ingest
from src.models import Customer, Delivery

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1",
    reason="Test d'intégration : export RUN_DB_TESTS=1 et démarrez MariaDB.",
)


@pytest.fixture
def session():
    session = Session()
    yield session
    session.close()


def test_ingestion_is_idempotent(session):
    df = pd.read_csv(DEFAULT_PROCESSED_PATH)

    ingest(df)
    first = (
        session.query(Customer).count(),
        session.query(Delivery).count(),
    )

    ingest(df)
    second = (
        session.query(Customer).count(),
        session.query(Delivery).count(),
    )

    assert first == (22, 23)
    assert second == first
