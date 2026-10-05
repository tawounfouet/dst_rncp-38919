from fastapi import FastAPI

app = FastAPI(title="parcelpulse-api-lab05")


@app.get("/health")
def health():
    return {"status": "ok", "app": "parcelpulse-api", "lab": "05"}
