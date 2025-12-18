from fastapi import FastAPI
from threading import Thread

from .storage import read_status
from .worker import run
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>simple-bot</title>
  <style>
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      background: #0f172a;
      color: #e5e7eb;
      display: flex;
      height: 100vh;
      align-items: center;
      justify-content: center;
      margin: 0;
    }
    .card {
      background: #020617;
      border: 1px solid #1e293b;
      border-radius: 12px;
      padding: 24px 28px;
      width: 360px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    h1 {
      margin: 0 0 8px 0;
      font-size: 1.2rem;
    }
    p {
      margin: 0 0 16px 0;
      font-size: 0.9rem;
      color: #94a3b8;
    }
    a {
      display: block;
      padding: 10px 12px;
      margin-top: 8px;
      text-decoration: none;
      color: #38bdf8;
      border: 1px solid #1e293b;
      border-radius: 8px;
      transition: background 0.15s ease;
    }
    a:hover {
      background: #020617;
    }
    footer {
      margin-top: 14px;
      font-size: 0.75rem;
      color: #64748b;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>simple-bot</h1>
    <p>Containerized RSS worker demo (DevOps).</p>

    <a href="/status">/status</a>
    <a href="/health">/health</a>
    <a href="/docs">/docs</a>

    <footer>running in container</footer>
  </div>
</body>
</html>
"""

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/status")
def status():
    return read_status()

@app.on_event("startup")
def start_worker():
    Thread(target=run, daemon=True).start()
