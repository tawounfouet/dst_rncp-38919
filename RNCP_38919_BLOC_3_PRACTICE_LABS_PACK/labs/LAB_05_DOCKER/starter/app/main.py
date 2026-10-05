from fastapi import FastAPI

app = FastAPI(title="parcelpulse-api-lab05-starter")


@app.get("/health")
def health():
    return {"status": "ok", "app": "parcelpulse-api", "lab": "05-starter"}
