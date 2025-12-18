# simple-bot

Ein kleiner, containerisierter Worker-Service zur Demonstration grundlegender DevOps-Praktiken.

Der Service ruft in regelmäßigen Abständen öffentliche RSS-Feeds ab, zählt die verfügbaren
Artikel und stellt den aktuellen Zustand über eine einfache HTTP-API bereit.

Link zum Testen(no index): https://simple-bot-kphc.onrender.com

## Entwicklungs- und Deployment-Workflow

1. Das Projekt wurde als Git-Repository mit einer klaren Struktur angelegt.
   Frühzeitig wurde ein Dockerfile ergänzt, um einen reproduzierbaren Build und
   eine konsistente Laufzeitumgebung sicherzustellen.

2. Für Continuous Integration wurde eine CI-Pipeline mit GitHub Actions eingerichtet
   (`.github/workflows/ci.yml`).
   Die Pipeline installiert die Abhängigkeiten, prüft, ob die Anwendung korrekt
   geladen werden kann, und verifiziert, dass ein Docker-Image erfolgreich gebaut
   werden kann.

3. Die Anwendung besteht aus einem kleinen Python-Worker und einem FastAPI-Service.
   Der Worker ruft periodisch öffentliche RSS-Feeds ab und speichert die Ergebnisse
   im JSON-Format, während die API Health- und Status-Endpoints bereitstellt.

4. Alle benötigten Abhängigkeiten sind in der Datei `requirements.txt` definiert.
   Sobald der Service lokal in Docker lauffähig ist, werden Änderungen committed
   und in das GitHub-Repository gepusht.

5. Nach jedem Push wird der GitHub-Actions-Workflow automatisch ausgeführt.
   Ein grüner Status zeigt an, dass der Service baubar und deploy-bereit ist.

6. Das Repository ist mit Render verbunden, welches das Docker-Image baut und den
   Service in der Cloud deployt.

7. Nach dem Deployment ist der Service öffentlich erreichbar und kann über die
   Endpoints `/health` und `/status` überprüft werden.

## Endpoints
- `GET /` – einfache Status-Startseite
- `GET /health` – Health-Check-Endpoint
- `GET /status` – aktueller Zustand mit Artikelanzahl im JSON-Format

## Deployment & DevOps
- Der Service ist mit Docker containerisiert
- CI wird über GitHub Actions umgesetzt und stellt sicher, dass das Projekt
  baubar und lauffähig ist
- Das Deployment erfolgt auf einer Managed-Cloud-Plattform (Render)
- Konfiguration erfolgt über Environment-Variablen
- Der Zustand wird außerhalb des Containers gespeichert, um sichere Neustarts
  zu ermöglichen

## Tech-Stack
- Python
- FastAPI
- Docker
- Git & GitHub
- GitHub Actions (CI)
- REST / JSON
- Öffentliche RSS-Feeds
- Render (Hosting)
