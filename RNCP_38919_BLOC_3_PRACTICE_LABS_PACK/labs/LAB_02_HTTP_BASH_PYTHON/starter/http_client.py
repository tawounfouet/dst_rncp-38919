#!/usr/bin/env python3
"""
LAB 02 — Starter : Client HTTP en Python standard (urllib)
Objectif : Envoyer une requête HTTP POST avec un payload JSON et lire la réponse.
"""
import json
import os
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen

api_url = os.getenv("API_URL", "http://localhost:8000")

# 1. Préparer les données d'entrée (dictionnaire Python)
payload = {
    "distance_km": 12.5,
    "package_weight_kg": 3.2,
}

# 2. Sérialiser en JSON et encoder en octets (bytes UTF-8)
# TODO: encodez 'payload' avec json.dumps().encode('utf-8')
encoded_data = json.dumps(payload).encode("utf-8")

# 3. Construire la requête HTTP POST avec l'en-tête Content-Type
# TODO: instanciez Request avec f"{api_url}/predict", data=..., headers=..., method="POST"
request = Request(
    f"{api_url}/predict",
    data=encoded_data,
    headers={"Content-Type": "application/json"},
    method="POST",
)

# 4. Envoyer la requête et afficher le statut et le corps de réponse
try:
    with urlopen(request) as response:
        print("Status code :", response.status)
        response_body = response.read().decode("utf-8")
        print("Réponse API :", response_body)
except URLError as err:
    print(f"❌ Erreur de connexion ({err}) : Impossible de joindre l'API sur {api_url}.")
    print("👉 Assurez-vous qu'un serveur écoute sur ce port, par exemple en lançant :")
    print("   python mock_server.py  (dans un autre terminal)")
    sys.exit(1)
