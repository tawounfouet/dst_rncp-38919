docker build -t parcelpulse-api .
docker run --rm -p 8000:8000 parcelpulse-api
docker ps
docker logs <container>
