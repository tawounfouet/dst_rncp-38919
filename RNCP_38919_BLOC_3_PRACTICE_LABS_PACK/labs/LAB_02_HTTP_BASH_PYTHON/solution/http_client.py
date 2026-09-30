import json
import os
from urllib.request import Request, urlopen

api_url = os.getenv("API_URL", "http://localhost:8000")
payload = {"distance_km": 12.5, "package_weight_kg": 3.2}
request = Request(
    f"{api_url}/predict",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urlopen(request) as response:
    print("status:", response.status)
    print("body:", response.read().decode("utf-8"))
