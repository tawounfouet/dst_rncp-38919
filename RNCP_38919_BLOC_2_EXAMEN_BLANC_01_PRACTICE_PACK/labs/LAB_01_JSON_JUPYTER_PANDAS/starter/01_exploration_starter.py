# LAB 01 — Starter (version script)
# Complétez les TODO.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "deliveries_lab.json"

# TODO 1 — charger le JSON
# Indice : df = pd.read_json(DATA_PATH)
raise NotImplementedError("TODO 1 : chargez le JSON dans df, puis supprimez ce raise.")

# TODO 2 — head / shape / columns / info

# TODO 3 — nulls et doublons

# TODO 4 — normaliser customer_city

# TODO 5 — visualiser late_delivery

# TODO 6 — histogramme distance_km