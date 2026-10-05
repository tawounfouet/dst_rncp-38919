from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from validation import validate_dataframe

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SOURCE = BASE_DIR.parent.parent / "LAB_01_JSON_JUPYTER_PANDAS" / "data" / "deliveries_lab.json"
DEFAULT_DB = BASE_DIR / "deliveries.sqlite"

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    customer_city TEXT,
    vehicle_type TEXT,
    distance_km REAL,
    traffic_level TEXT,
    weather TEXT,
    delivery_minutes INTEGER,
    late_delivery INTEGER
)
"""


def ensure_table(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text(CREATE_TABLE))


def existing_ids(engine: Engine) -> set[int]:
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT delivery_id FROM deliveries")).fetchall()
    return {row[0] for row in rows}


def ingest(df: pd.DataFrame, engine: Engine) -> int:
    """Insère les lignes dont le delivery_id est inconnu. Retourne le nombre inséré."""
    validate_dataframe(df)
    ensure_table(engine)

    known = existing_ids(engine)
    new = df[~df["delivery_id"].isin(known)]

    if not new.empty:
        new.to_sql("deliveries", engine, if_exists="append", index=False)

    return len(new)


def count_rows(engine: Engine) -> int:
    with engine.connect() as conn:
        return conn.execute(text("SELECT COUNT(*) FROM deliveries")).scalar_one()


def main() -> None:
    engine = create_engine(f"sqlite:///{DEFAULT_DB}")
    df = pd.read_json(DEFAULT_SOURCE).drop_duplicates(subset=["delivery_id"]).copy()

    inserted = ingest(df, engine)
    again = ingest(df, engine)

    print(f"1re ingestion : {inserted} ligne(s) insérée(s)")
    print(f"2e  ingestion : {again} ligne(s) insérée(s)  <- doit valoir 0")
    print(f"total en base : {count_rows(engine)}")


if __name__ == "__main__":
    main()
