# simple-bot

A minimal DevOps demonstration of a containerized RSS worker service.

The service runs a background worker that periodically fetches public RSS feeds
and exposes its current state via a small HTTP API.

## Endpoints
- `GET /health` – health check
- `GET /status` – latest collected article counts

## Configuration
Configuration is provided via environment variables.
State is stored in `/data` and can be backed by a persistent volume.
