#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example — edit secrets before production use."
fi

echo "Building and starting the local stack..."
docker compose up -d --build
echo
echo "API (via nginx):  http://localhost:8080/health"
echo "Prometheus:       http://localhost:9090"
echo "Grafana:          http://localhost:3000  (admin / value of GRAFANA_ADMIN_PASSWORD)"
echo "cAdvisor:         http://localhost:8081"
echo "Alertmanager:     http://localhost:9093"
