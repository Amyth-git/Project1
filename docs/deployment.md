# Deployment

## Prerequisites

- Docker Desktop or Docker Engine + Compose v2
- Python 3.12 (for local tests)
- AWS CLI + Terraform 1.6+ (for cloud)
- GitHub repository with Actions enabled (for CI/CD)

## Local stack

```bash
cd Project1
cp .env.example .env
make bootstrap
curl -s http://localhost:8080/health
```

Rolling update of only the API:

```bash
bash scripts/deploy.sh local
```

Stop:

```bash
make down
```

## CI

On every push/PR, `.github/workflows/ci.yml`:

1. Installs Python deps
2. Runs Ruff and pytest
3. Builds the Docker image
4. Scans it with Trivy (fails on unfixed HIGH/CRITICAL)

## Cloud (AWS)

1. Create an IAM user or OIDC role with ECS, ECR, VPC, IAM, CloudWatch, ELB permissions.
2. Store `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as GitHub Actions secrets (or use OIDC).
3. Bootstrap infrastructure:

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# edit api_key and region
terraform init
terraform apply
```

4. Push the first image (ECR URL is a Terraform output):

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker build -t project1-api:latest app
docker tag project1-api:latest <ecr_repository_url>:latest
docker push <ecr_repository_url>:latest
aws ecs update-service --cluster project1-staging --service project1-staging-api --force-new-deployment
```

5. Tag a release (`v1.0.0`) or run the **Deploy** workflow to build, push, and roll ECS.

The ALB DNS name is in `terraform output alb_dns_name`. Health checks hit `/health`.

## GitHub environments

Create a `staging` (and optionally `production`) GitHub Environment. The deploy job uses it for protection rules (required reviewers, wait timer).
