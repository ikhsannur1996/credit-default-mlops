# RUNBOOK — Daily Demo

## Start

```bash
cd /opt/credit-default-mlops
source .venv/bin/activate
```

## Check services

```bash
docker ps
sudo systemctl status k3s --no-pager
kubectl get pods -A
```

## API

```bash
kubectl port-forward \
  -n credit-default \
  svc/credit-default-api 8000:8000
```

Then:

```bash
curl http://127.0.0.1:8000/health
```

## Grafana

```bash
kubectl port-forward \
  -n monitoring \
  svc/monitoring-grafana 3000:80
```

## Prometheus

```bash
kubectl port-forward \
  -n monitoring \
  svc/monitoring-kube-prometheus-prometheus 9090:9090
```

## MLflow

```bash
ssh -L 5000:127.0.0.1:5000 USER@VM_IP
```

## Drift

```bash
python src/generate_drift.py
python src/drift.py
```

## Retraining

```bash
python src/train.py
python src/evaluate.py
```

## Rollback Kubernetes

```bash
kubectl rollout history deployment/credit-default-api -n credit-default
kubectl rollout undo deployment/credit-default-api -n credit-default
```
