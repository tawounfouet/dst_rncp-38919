docker build -t parcelpulse-api .
docker login
docker tag parcelpulse-api:latest USER/parcelpulse-api:latest
docker push USER/parcelpulse-api:latest
docker pull USER/parcelpulse-api:latest
