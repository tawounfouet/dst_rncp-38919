from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    # TODO: colonnes + relation
    pass

class Delivery(Base):
    __tablename__ = "deliveries"

    # TODO: colonnes + FK + relation
    pass
