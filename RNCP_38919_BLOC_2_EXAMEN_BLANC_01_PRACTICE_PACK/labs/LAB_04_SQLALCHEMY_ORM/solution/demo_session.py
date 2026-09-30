from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Customer, Delivery

DATABASE_URL = "mysql+pymysql://practice_user:practice_password@localhost:3306/practice"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine, checkfirst=True)

Session = sessionmaker(bind=engine)
session = Session()

customer = Customer(customer_id=1, customer_city="paris")
session.add(customer)
session.commit()

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
session.add(delivery)
session.commit()

print(session.query(Customer).all())
print(session.query(Delivery).all())

session.close()
