from fastapi import FastAPI
from threading import Thread

from .storage import read_status
from .worker import run

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/status")
def status():
    return read_status()

@app.on_event("startup")
def start_worker():
    Thread(target=run, daemon=True).start()
