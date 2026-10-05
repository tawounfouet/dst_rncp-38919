from pathlib import Path

import pandas as pd

from src.database import Session
from src.models import Customer, Delivery

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "deliveries_clean.csv"


def ingest(df: pd.DataFrame) -> tuple[int, int]:
    """Ingère clients puis livraisons. Idempotent : n'ajoute pas les ID déjà présents.

    Retourne (nombre de clients insérés, nombre de livraisons insérées).
    """
    session = Session()
    inserted_customers = 0
    inserted_deliveries = 0

    try:
        customers = df[["customer_id", "customer_city"]].drop_duplicates(
            subset=["customer_id"]
        )

        for row in customers.to_dict(orient="records"):
            customer_id = int(row["customer_id"])
            if session.query(Customer).filter_by(customer_id=customer_id).first():
                continue
            session.add(
                Customer(
                    customer_id=customer_id,
                    customer_city=str(row["customer_city"]),
                )
            )
            inserted_customers += 1

        session.commit()

        for row in df.to_dict(orient="records"):
            delivery_id = int(row["delivery_id"])
            if session.query(Delivery).filter_by(delivery_id=delivery_id).first():
                continue
            session.add(
                Delivery(
                    delivery_id=delivery_id,
                    customer_id=int(row["customer_id"]),
                    vehicle_type=str(row["vehicle_type"]),
                    distance_km=float(row["distance_km"]),
                    traffic_level=str(row["traffic_level"]),
                    weather=str(row["weather"]),
                    delivery_minutes=int(row["delivery_minutes"]),
                    late_delivery=int(row["late_delivery"]),
                )
            )
            inserted_deliveries += 1

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

    return inserted_customers, inserted_deliveries


def main() -> None:
    df = pd.read_csv(DEFAULT_PROCESSED_PATH)
    inserted_customers, inserted_deliveries = ingest(df)
    print(
        f"Ingestion completed: "
        f"{inserted_customers} customer(s), "
        f"{inserted_deliveries} delivery(ies) inserted"
    )


if __name__ == "__main__":
    main()
