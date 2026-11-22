# Project handover

## What was delivered

1. **Application** — FastAPI service with health, readiness, CRUD demo, JSON logs, Prometheus metrics, tests
2. **Containerization** — multi-stage Dockerfile, Compose stack with resource limits and health checks
3. **Reverse proxy** — nginx with security headers, rate limit, metrics blocked from the public port
4. **CI/CD** — GitHub Actions: lint, test, image build, Trivy scan; tag/manual deploy to ECS
5. **Cloud** — Terraform for VPC, NAT, ALB, ECR, ECS Fargate, IAM, CloudWatch
6. **Monitoring** — Prometheus, Alertmanager, Grafana (provisioned dashboard), cAdvisor, node-exporter
7. **Security** — non-root, read-only FS, internal networks, API key on mutations, secret hygiene
8. **Docs** — architecture, deploy, security, monitoring, this handover

## How to demo (15 minutes)

1. `make bootstrap` and show `http://localhost:8080/health`
2. Create an item: `curl -X POST http://localhost:8080/items -H 'Content-Type: application/json' -d '{"name":"demo"}'`
3. Open Prometheus targets (all UP) and Grafana **Project1 Overview**
4. Walk through `.github/workflows/ci.yml` and `terraform/ecs.tf`
5. Mention production follow-ups from `docs/security.md`

## Repository map

```
app/                 API source, tests, Dockerfile
nginx/               Reverse proxy config
monitoring/          Prometheus, Alertmanager, Grafana
terraform/           AWS infrastructure
scripts/             bootstrap + local rolling deploy
.github/workflows/   CI and Deploy
docs/                Technical documentation
```

## Operations runbook (short)

| Issue | Check |
| --- | --- |
| API 502 | `docker compose ps` and `docker compose logs app` |
| Grafana empty graphs | Confirm Prometheus target `project1-api` is UP; generate traffic |
| ECS deploy stuck | Task stopped reason in ECS console; image exists in ECR; `/health` returns 200 |
| Terraform apply fails on image | Push an image to ECR then `force-new-deployment` |

## Credentials to rotate after handover

- `.env` `API_KEY` and Grafana password
- AWS access keys used by Actions
- Terraform `api_key`

Do not reuse the example values (`change-me-in-production`, `admin`/`admin`) outside a local demo.
