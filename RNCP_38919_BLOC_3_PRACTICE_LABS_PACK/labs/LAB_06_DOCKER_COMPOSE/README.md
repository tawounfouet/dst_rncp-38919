# LAB 06 — Docker Compose, volumes et depends_on

Construire une stack :

```text
app
prometheus
grafana
```

Contraintes :

- volume `/models` ;
- `prometheus depends_on app` ;
- `grafana depends_on prometheus`.
