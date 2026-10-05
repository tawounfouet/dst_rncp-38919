# LAB 04 — Mode examen

⏱ **35 min**. Complétez `starter/models.py`, puis écrivez la session.

## Checklist chronométrée

- [ ] 0–5 : démarrer la DB du LAB 03
- [ ] 5–15 : `Customer` (PK, ville)
- [ ] 15–25 : `Delivery` (PK, FK, colonnes, relation)
- [ ] 25–30 : `config.py` + `DATABASE_URL` depuis `.env`
- [ ] 30–35 : session, `create_all`, insert, `query`

## Questions de contrôle

1. Différence entre `Column(Integer, primary_key=True)` et `unique=True` ?
2. Que fait `relationship(back_populates=...)` des deux côtés ?
3. Pourquoi `merge` plutôt que `add` pour un script réexécutable ?
4. Le port dans `DATABASE_URL` : hôte ou conteneur ?

## Solution

<details>
<summary>models.py</summary>

```python
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
```
</details>

<details>
<summary>config.py</summary>

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER','practice_user')}"
    f":{os.getenv('DB_PASSWORD','practice_password')}"
    f"@{os.getenv('DB_HOST','localhost')}"
    f":{os.getenv('DB_PORT','3306')}"
    f"/{os.getenv('DB_NAME','practice')}"
)
```
</details>

<details>
<summary>demo_session.py</summary>

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base, Customer, Delivery

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine, checkfirst=True)

session = sessionmaker(bind=engine)()
session.merge(Customer(customer_id=1, customer_city="paris"))
session.merge(Delivery(
    delivery_id=1, customer_id=1, vehicle_type="bike", distance_km=4.2,
    traffic_level="high", weather="rain", delivery_minutes=38, late_delivery=1,
))
session.commit()
print(session.query(Customer).all())
print(session.query(Delivery).all())
session.close()
```
</details>

## Auto-évaluation

| Point | OK ? |
|---|---|
| Je crée des modèles avec `declarative_base` | |
| Je pose la FK et la relation des deux côtés | |
| Je configure l'URL via `.env` (pas en dur) | |
| Je sais qu'un script `merge` est réexécutable | |
| Je vérifie en base avec `mariadb` | |
