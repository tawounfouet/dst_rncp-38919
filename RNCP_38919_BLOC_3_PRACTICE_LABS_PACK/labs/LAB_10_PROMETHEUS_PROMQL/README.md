# LAB 10 — Prometheus et PromQL

1. Exposer `/metrics` depuis FastAPI.
2. Compléter `prometheus.yml`.
3. Vérifier que la target est `UP`.
4. Identifier une vraie métrique depuis `/metrics`.
5. Tester une requête simple, puis `rate` / `sum by` si approprié.

Ne pas inventer les noms de métriques.

## Note sur la résolution réseau de la cible (Scrape Target)
* **Sous Docker Compose :** La cible `app:8000` résout automatiquement le nom du conteneur FastAPI sur le réseau interne.
* **En local (Prometheus natif sur l'hôte) :** Remplacer `app:8000` par `localhost:8000`.
* **Prometheus conteneurisé scrapant l'hôte :** Remplacer par `host.docker.internal:8000`.
