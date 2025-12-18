import json
from pathlib import Path
from datetime import datetime, timezone

DATA_PATH = Path("/data/status.json")

def read_status():
    if not DATA_PATH.exists():
        return {"updated_at": None, "sources": {}}
    return json.loads(DATA_PATH.read_text())

def write_status(sources: dict):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "sources": sources,
    }
    DATA_PATH.write_text(json.dumps(payload, indent=2))
