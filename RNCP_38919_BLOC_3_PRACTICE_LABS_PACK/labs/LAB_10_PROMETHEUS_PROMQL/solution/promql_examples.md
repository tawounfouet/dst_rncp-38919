# PromQL — Requêtes et Patterns de Référence

Ce document rassemble les requêtes PromQL réelles issues de l'instrumentation FastAPI (`prometheus-fastapi-instrumentator`) et du scraping Prometheus.

---

## 1. Architecture de collecte et interrogation

```mermaid
flowchart LR
    App[FastAPI /metrics] <-- scrape 15s --- Prom[Prometheus Server]
    Prom --> Eval[Moteur d'évaluation PromQL]
    Eval --> Graf[Grafana Panels / Alertes]
```

```text
+---------------------+     scrape (15s)     +--------------------+
|  FastAPI /metrics   | <------------------- |  Prometheus Server |
+---------------------+                      +--------------------+
                                                        |
                                                        v
                                             +--------------------+
                                             | Moteur PromQL      |
                                             +--------------------+
                                                        |
                                                        v
                                             +--------------------+
                                             | Tableaux Grafana   |
                                             +--------------------+
```

---

## 2. Vérification de l'état du service (Liveness)

Vérifie si la cible configurée dans `prometheus.yml` est joignable et saine :

```promql
# Renvoie 1 si l'API est UP, 0 si DOWN
up{job="fastapi"}
```

---

## 3. Requêtes sur les compteurs HTTP (`http_requests_total`)

### Débit global de requêtes par seconde (RPS)
Calcule le taux moyen de requêtes par seconde sur les 5 dernières minutes :

```promql
sum(rate(http_requests_total[5m]))
```

### Débit groupé par statut HTTP (ex: 200, 422, 500)
Permet de visualiser la proportion d'erreurs ou de succès :

```promql
sum by (status) (rate(http_requests_total[5m]))
```

### Débit groupé par handler / route (ex: `/predict`, `/health`)
Permet d'identifier quel endpoint consomme le plus de trafic :

```promql
sum by (handler) (rate(http_requests_total[5m]))
```

### Débit groupé par méthode HTTP (ex: GET, POST)
```promql
sum by (method) (rate(http_requests_total[5m]))
```

---

## 4. Requêtes sur la latence et les percentiles (Histogram)

L'instrumentateur expose des buckets de durée d'exécution des requêtes :

### Temps moyen de réponse par requête (en secondes)
```promql
sum(rate(http_request_duration_seconds_sum[5m]))
/
sum(rate(http_request_duration_seconds_count[5m]))
```

### 95e percentile de latence (p95)
Indique la latence maximale subie par 95% des utilisateurs :

```promql
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))
```

---

## 5. Métriques système de l'application

### Consommation mémoire du processus FastAPI (en mégaoctets)
```promql
process_resident_memory_bytes{job="fastapi"} / 1024 / 1024
```

### Utilisation CPU cumulée
```promql
rate(process_cpu_seconds_total{job="fastapi"}[5m])
```
