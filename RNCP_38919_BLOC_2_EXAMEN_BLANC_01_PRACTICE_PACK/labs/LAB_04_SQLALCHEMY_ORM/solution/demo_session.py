from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL
from models import Base, Customer, Delivery


def main() -> None:
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine, checkfirst=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    customer = Customer(customer_id=1, customer_city="paris")
    session.merge(customer)

    delivery = Delivery(
        delivery_id=1,
        customer_id=1,
        vehicle_type="bike",
        distance_km=4.2,
        traffic_level="high",
        weather="rain",
        delivery_minutes=38,
        late_delivery=1,
    )
    session.merge(delivery)
    session.commit()

    print(session.query(Customer).all())
    print(session.query(Delivery).all())

    session.close()


if __name__ == "__main__":
    main()
