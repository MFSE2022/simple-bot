from fastapi import FastAPI
from threading import Thread
import json

from .storage import read_status
from .worker import run
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()
CSS = """
  <style>
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      background: #0f172a;
      color: #e5e7eb;
      display: flex;
      min-height: 100vh;
      align-items: center;
      justify-content: center;
      margin: 0;
      padding: 24px;
    }
    .card {
      background: #020617;
      border: 1px solid #1e293b;
      border-radius: 12px;
      padding: 24px 28px;
      width: min(720px, 100%);
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    h1 { margin: 0 0 8px 0; font-size: 1.2rem; }
    p  { margin: 0 0 16px 0; font-size: 0.9rem; color: #94a3b8; }
    a {
      display: inline-block;
      padding: 10px 12px;
      margin: 8px 8px 0 0;
      text-decoration: none;
      color: #38bdf8;
      border: 1px solid #1e293b;
      border-radius: 8px;
      transition: background 0.15s ease;
    }
    a:hover { background: #0b1220; }
    .badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid #1e293b;
      font-size: 0.8rem;
      margin-top: 8px;
    }
    .ok { color: #86efac; }
    .fail { color: #fca5a5; }
    pre {
      margin: 14px 0 0 0;
      padding: 14px;
      background: #0b1220;
      border: 1px solid #1e293b;
      border-radius: 10px;
      overflow: auto;
      font-size: 0.85rem;
      line-height: 1.35;
    }
    footer {
      margin-top: 16px;
      font-size: 0.75rem;
      color: #64748b;
      text-align: center;
    }
  </style>
"""
def page(title: str, subtitle: str, content_html: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  {CSS}
</head>
<body>
  <div class="card">
    <h1>{title}</h1>
    <p>{subtitle}</p>

    <a href="/">Home</a>
    <a href="/health">Health</a>
    <a href="/status">Status</a>
    <a href="/docs">Docs</a>

    {content_html}

    <footer>simple-bot</footer>
  </div>
</body>
</html>
"""
@app.get("/", response_class=HTMLResponse)
def root():
    return page(
        "simple-bot",
        "Containerized RSS worker demo (DevOps).",
        "<div class='badge ok'>running</div>",
    )

@app.get("/health.json", response_class=JSONResponse)
def health_json():
    return {"status": "ok"}
@app.get("/health", response_class=HTMLResponse)
def health_page():
    return page(
        "Health",
        "Basic health check endpoint.",
        "<div class='badge ok'>status: ok</div>",
    )

@app.get("/status", response_class=HTMLResponse)
def status_page():
    status = read_status()
    pretty = json.dumps(status, indent=2, ensure_ascii=False)
    return page(
        "Status",
        "Latest collected article counts (JSON).",
        f"<pre>{pretty}</pre>",
    )

@app.get("/status.json", response_class=JSONResponse)
def status_json():
    return read_status()

@app.on_event("startup")
def start_worker():
    Thread(target=run, daemon=True).start()
