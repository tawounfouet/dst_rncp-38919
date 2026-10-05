#!/usr/bin/env python3
"""
LAB 02 — Solution : Client HTTP en Python standard (urllib)
"""
import json
import os
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen

api_url = os.getenv("API_URL", "http://localhost:8000")
payload = {"distance_km": 12.5, "package_weight_kg": 3.2}

request = Request(
    f"{api_url}/predict",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

try:
    with urlopen(request) as response:
        print("status:", response.status)
        print("body:", response.read().decode("utf-8"))
except URLError as err:
    print(f"❌ Erreur de connexion ({err}): Impossible de joindre l'API sur {api_url}.")
    print("👉 Assurez-vous qu'un serveur écoute sur ce port, par exemple en lançant :")
    print("   python mock_server.py  (dans un autre terminal ou en arrière-plan)")
    print("   OU")
    print("   uvicorn app:app --port 8000 (depuis labs/LAB_03_FASTAPI_PYDANTIC_JOBLIB/solution)")
    sys.exit(1)
