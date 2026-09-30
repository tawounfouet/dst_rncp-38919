# LAB 02 — ETL Python

**Temps cible : 35 min**

## Mission
Implémenter :
```python
extract()
validate_schema()
transform()
save_processed()
```

Contraintes :
- fichier absent → `FileNotFoundError` ;
- colonne requise absente → `ValueError` ;
- dédupliquer sur `delivery_id` ;
- normaliser `customer_city` ;
- imputer `distance_km` par médiane ;
- imputer `traffic_level` et `weather` par `unknown`.
