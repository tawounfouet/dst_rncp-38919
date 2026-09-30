REQUIRED_COLUMNS = {
    "delivery_id",
    "customer_id",
    "customer_city",
    "vehicle_type",
    "distance_km",
    "traffic_level",
    "weather",
    "delivery_minutes",
    "late_delivery",
}

def validate_dataframe(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    if df["delivery_id"].isna().any():
        raise ValueError("Null delivery_id detected")

    if df["delivery_id"].duplicated().any():
        raise ValueError("Duplicate delivery_id detected")
