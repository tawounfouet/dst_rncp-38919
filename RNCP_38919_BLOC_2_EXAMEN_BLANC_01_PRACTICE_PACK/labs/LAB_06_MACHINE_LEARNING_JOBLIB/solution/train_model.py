from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("data/deliveries_ml.csv")

numeric_features = ["distance_km"]
categorical_features = ["customer_city", "vehicle_type", "traffic_level", "weather"]

X = df[numeric_features + categorical_features]
y = df["late_delivery"]

preprocessing = ColumnTransformer(
    transformers=[
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
        ]), numeric_features),
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]), categorical_features),
    ]
)

pipeline = Pipeline([
    ("preprocessing", preprocessing),
    ("model", LogisticRegression(max_iter=1000)),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

pipeline.fit(X_train, y_train)
pred = pipeline.predict(X_test)

print("accuracy :", accuracy_score(y_test, pred))
print("precision:", precision_score(y_test, pred, zero_division=0))
print("recall   :", recall_score(y_test, pred, zero_division=0))
print("f1       :", f1_score(y_test, pred, zero_division=0))

Path("models").mkdir(parents=True, exist_ok=True)
joblib.dump(pipeline, "models/model.joblib")
