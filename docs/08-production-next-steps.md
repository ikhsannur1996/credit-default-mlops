# 08 - Production Next Steps

This project is intentionally simple.

For a real production system, add these incrementally.

## Security

- HTTPS
- Authentication
- API authentication
- Secrets manager
- Network restrictions
- Non-root containers

## MLflow

Replace:

```text
SQLite + local mlruns
```

with:

```text
PostgreSQL/MySQL
+
S3-compatible object storage
```

## Deployment

Current:

```text
Docker Compose
```

Possible future:

```text
Kubernetes
```

Only introduce Kubernetes when there is a real operational need.

## Monitoring

Current:

```text
MLflow metrics + artifacts
```

Possible future:

```text
Prometheus + Grafana
```

for infrastructure and service observability.

## Data pipeline

Possible future:

```text
Airflow
dbt
Spark
Feature Store
```

## CI/CD

Current CI checks Python syntax.

Future:

```text
GitHub Actions
    ↓
Tests
    ↓
Build image
    ↓
Security scan
    ↓
Deploy
    ↓
Smoke test
```

## Retraining

Current:

```text
manual command
or AUTO_RETRAIN=1
```

Future:

```text
Scheduler
   ↓
Drift detected
   ↓
Retraining
   ↓
Evaluation gate
   ↓
Model approval
   ↓
Deployment
```

## Model governance

For financial/credit use cases, add:

- model approval
- model version traceability
- training dataset versioning
- explainability
- audit logs
- model risk controls
- rollback
- human approval before production promotion
