# Project1

Automated **deployment** and **infrastructure monitoring** system: a containerized API, Compose-based local platform, GitHub Actions CI/CD, Terraform on AWS (ECS Fargate + ALB), security defaults, and Prometheus/Grafana.

## Quick start

```bash
cp .env.example .env
make bootstrap
curl -s http://localhost:8080/health
```

| Surface | URL |
| --- | --- |
| API (nginx) | http://localhost:8080 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 (admin / admin unless you change `.env`) |
| Alertmanager | http://localhost:9093 |

## What is in this repo

- **Docker** — multi-stage API image, nginx, Prometheus, Grafana, Alertmanager, cAdvisor, node-exporter
- **CI/CD** — lint, tests, image build, Trivy scan, ECS rolling deploy on version tags
- **Cloud** — Terraform VPC, private ECS tasks, ALB, ECR with scan-on-push
- **Security** — non-root, read-only containers, internal networks, API keys, header/rate-limit at nginx
- **Monitoring** — scrape configs, alert rules, provisioned Grafana dashboard
- **Docs** — [architecture](docs/architecture.md), [deployment](docs/deployment.md), [security](docs/security.md), [monitoring](docs/monitoring.md), [handover](docs/handover.md)

## Local development

```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
uvicorn project1.main:app --reload --app-dir src
```

## Cloud deploy (summary)

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
terraform init && terraform apply
# push image to the ECR URL from terraform output, then:
# git tag v1.0.0 && git push --tags
```

Full steps: [docs/deployment.md](docs/deployment.md).

## License

Provided as an educational/handover project. Use and adapt as needed.
