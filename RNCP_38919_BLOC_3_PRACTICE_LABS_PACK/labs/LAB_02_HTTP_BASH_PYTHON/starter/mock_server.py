#!/usr/bin/env python3
"""
Mock Server minimal pour le LAB 02 (Zero-dependency HTTP Server).
Permet de tester curl et urllib sans avoir besoin d'installer FastAPI ou Uvicorn.
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000


class MockAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {"status": "ok", "service": "mock-delivery-api"})
        else:
            self._send_json(404, {"detail": f"Route GET {self.path} non trouvée. Routes valides : /health"})

    def do_POST(self):
        if self.path == "/predict":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode("utf-8")) if post_data else {}
                dist = float(payload.get("distance_km", 10.0))
                weight = float(payload.get("package_weight_kg", 2.0))
                # Calcul de simulation : durée de livraison estimée en minutes
                prediction = round(dist * 1.5 + weight * 0.8 + 5.0, 2)
                self._send_json(
                    200,
                    {
                        "prediction": prediction,
                        "unit": "minutes",
                        "model_version": "mock-delivery-v1",
                        "received_features": payload,
                    },
                )
            except Exception as err:
                self._send_json(400, {"error": f"JSON invalide ou champs manquants : {err}"})
        else:
            self._send_json(404, {"detail": f"Route POST {self.path} non trouvée. Routes valides : /predict"})

    def log_message(self, format, *args):
        sys.stderr.write(f"[Mock Server :8000] {self.address_string()} - {format % args}\n")


def run(port: int = PORT):
    server_address = ("127.0.0.1", port)
    try:
        httpd = HTTPServer(server_address, MockAPIHandler)
    except OSError as err:
        print(f"❌ Impossible d'écouter sur le port {port} : {err}")
        print("   Vérifiez si un autre serveur (FastAPI, Uvicorn, etc.) tourne déjà sur ce port.")
        sys.exit(1)

    print(f"🚀 Serveur Mock démarré avec succès sur http://127.0.0.1:{port}")
    print("   Endpoints disponibles :")
    print(f"   - GET  http://localhost:{port}/health")
    print(f"   - POST http://localhost:{port}/predict")
    print("   (Laissez ce terminal ouvert ou appuyez sur Ctrl+C pour arrêter le serveur)")
    print("-" * 65)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt propre du serveur mock.")
        httpd.server_close()


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run(port_arg)
