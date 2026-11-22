#!/usr/bin/env bash
# Rolling deploy of the API container on a host that already runs this compose stack.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

IMAGE_TAG="${1:-latest}"
export IMAGE_TAG

docker compose pull app || true
docker compose build app
docker compose up -d --no-deps --force-recreate app
docker compose exec -T app python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
echo "Local rolling deploy complete (tag=${IMAGE_TAG})."
