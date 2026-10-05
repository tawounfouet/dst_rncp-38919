# LAB 01 — Solution de référence (version script)

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "deliveries_lab.json"

# --- Chargement -----------------------------------------------------------
df = pd.read_json(DATA_PATH)
print(df.head())

# --- Structure ------------------------------------------------------------
print(df.shape)
print(df.columns.tolist())
df.info()

# --- Qualité des données --------------------------------------------------
print(df.isna().sum())
print("Doublons:", df.duplicated().sum())

# --- Normalisation de customer_city --------------------------------------
df["customer_city"] = (
    df["customer_city"].astype("string").str.strip().str.lower()
)
print(df["customer_city"].value_counts(dropna=False))

# --- Visualisations -------------------------------------------------------
df["late_delivery"].value_counts().sort_index().plot(kind="bar")
plt.title("Distribution de late_delivery")
plt.show()

df["distance_km"].hist()
plt.title("Distribution de distance_km")
plt.show()