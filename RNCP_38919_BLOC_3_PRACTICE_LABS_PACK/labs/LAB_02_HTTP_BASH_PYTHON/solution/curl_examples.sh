curl -i http://localhost:8000/health
curl -X POST -H "Content-Type: application/json" -d '{"distance_km":12.5,"package_weight_kg":3.2}' http://localhost:8000/predict
