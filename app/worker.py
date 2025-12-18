import os
import time
import requests

from .storage import write_status

FEEDS = [
    ("Digital", "https://www.nachrichten.at/storage/rss/rss/digital.xml"),
    ("Linz", "https://www.nachrichten.at/storage/rss/rss/linz.xml"),
    ("Wirtschaft", "https://www.nachrichten.at/storage/rss/rss/wirtschaft.xml"),
]

def count_items(xml: str) -> int:
    # RSS: <item>, Atom: <entry>
    return xml.count("<item>") + xml.count("<entry>")

def run():
    interval = int(os.getenv("INTERVAL_SECONDS", "600"))
    timeout = int(os.getenv("HTTP_TIMEOUT_SECONDS", "10"))

    while True:
        results = {}
        for name, url in FEEDS:
            try:
                r = requests.get(url, timeout=timeout, headers={"User-Agent": "demo-worker/1.0"})
                r.raise_for_status()
                results[name] = {"url": url, "articles": count_items(r.text), "ok": True}
            except Exception as e:
                results[name] = {"url": url, "articles": None, "ok": False, "error": str(e)}
        write_status(results)
        time.sleep(interval)
