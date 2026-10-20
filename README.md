# Customer Accounts Microservice — Agile Final Project

[![CI Build](https://github.com/harshalsuryawanshi23/agile-final-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/harshalsuryawanshi23/agile-final-project/actions/workflows/ci-build.yaml)

A learning capstone demonstrating Agile planning, RESTful account management, automated tests, CI, security headers, containerization, and Kubernetes deployment.

> CI runs the unit tests and lint checks, exercises the REST CRUD endpoints with cURL, builds the Docker image, deploys it to a temporary Kind cluster, and runs the Tekton CD PipelineRun. Captured runtime logs are saved under `evidence/`. The temporary cluster is deleted after the workflow; this repo does not host a persistent live endpoint.

## Features
- Create, read, list, update, and delete customer accounts through a REST API.
- JSON request validation and HTTP status codes.
- Unit tests using nose/coverage, plus Flake8 and Pylint lint checks.
- GitHub Actions continuous integration.
- Talisman security headers and a configurable CORS policy.
- Docker image and Kubernetes Deployment/Service manifests.

## Quick start
```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python server.py
```
The service listens on port 8080.

## Verify
```bash
nosetests --with-coverage --cover-package=service
flake8 service tests server.py
pylint service tests server.py
```

## Docker and Kubernetes
```bash
docker build -t accounts:1.0 .
docker run --rm -p 8080:8080 accounts:1.0
kubectl apply -f k8s/
kubectl get deployment,pods,replicasets,services -o wide
```

## Repository map
- `.github/ISSUE_TEMPLATE/user-story.md`: reusable story template
- `.github/workflows/ci-build.yaml`: CI workflow
- `setup.cfg`: test and lint configuration
- `service/`, `tests/`: Flask API and tests
- `Dockerfile`, `k8s/`: container and Kubernetes configuration
- `evidence/`: cURL examples and response/evidence templates
