.PHONY: help bootstrap up down logs test lint scan fmt

help:
	@echo "make bootstrap  - copy .env and start the full local stack"
	@echo "make up         - docker compose up -d --build"
	@echo "make down       - stop the stack"
	@echo "make logs       - follow API logs"
	@echo "make test       - run unit tests"
	@echo "make lint       - ruff check"
	@echo "make scan       - trivy image scan (requires trivy + built image)"

bootstrap:
	bash scripts/bootstrap.sh

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f app nginx

test:
	cd app && pip install -q -r requirements-dev.txt && pytest

lint:
	cd app && ruff check src tests

scan:
	docker build -t project1-api:local app
	trivy image --severity HIGH,CRITICAL project1-api:local
