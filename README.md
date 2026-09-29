# Credit Default MLOps — Simple End-to-End

Personal MLOps project running on **one Ubuntu VM**.

## Stack

- GitLab CE + GitLab Runner
- Python + JupyterLab
- Synthetic Credit Default Data
- Scikit-learn
- MLflow
- FastAPI
- Docker
- k3s Kubernetes
- Prometheus
- Grafana
- GitLab CI/CD

## Architecture

```text
                 GitLab
                   │
                   ▼
                 CI/CD
                   │
                   ▼
             Docker Image
                   │
                   ▼
                  k3s
                   │
                   ▼
                FastAPI
              /predict
                   │
          ┌────────┴────────┐
          ▼                 ▼
     Prometheus          MLflow
          │
          ▼
       Grafana

Jupyter → Data → Train → MLflow → Model → FastAPI
                         ▲
                         │
                    Drift check
```

## 8 stages

1. VM + Docker
2. GitLab + Jupyter
3. Data + Model
4. MLflow
5. FastAPI + Docker
6. Kubernetes
7. Prometheus + Grafana
8. CI/CD + Drift

## Quick start

See `SETUP.md`.

The project is deliberately small. It avoids PostgreSQL, Airflow, Kafka, MinIO, Terraform, ArgoCD, and multi-node Kubernetes.


## Public IP access

See `PUBLIC-IP.md` and `SETUP.md` for public VM access, UFW rules, provider firewall rules, and service URLs. Kubernetes API port 6443 is intentionally not exposed publicly.


## Public Kubernetes monitoring

Kubernetes monitoring is exposed through:

- Grafana: `http://PUBLIC_IP:30300`
- Prometheus: `http://PUBLIC_IP:30090`

See `KUBERNETES-PUBLIC-MONITORING.md`.
