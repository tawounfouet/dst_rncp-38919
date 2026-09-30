from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    customer_city = Column(String(100), nullable=False)

    deliveries = relationship("Delivery", back_populates="customer")

class Delivery(Base):
    __tablename__ = "deliveries"

    delivery_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    vehicle_type = Column(String(50), nullable=False)
    distance_km = Column(Float, nullable=False)
    traffic_level = Column(String(50), nullable=False)
    weather = Column(String(50), nullable=False)
    delivery_minutes = Column(Integer, nullable=False)
    late_delivery = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="deliveries")
