# Public IP Quick Reference

After setup:

```bash
PUBLIC_IP=$(curl -4 -s ifconfig.me)
echo $PUBLIC_IP
```

## Services

| Service | URL |
|---|---|
| GitLab | `http://PUBLIC_IP/` |
| FastAPI | `http://PUBLIC_IP:8000/docs` |
| FastAPI health | `http://PUBLIC_IP:8000/health` |
| FastAPI metrics | `http://PUBLIC_IP:8000/metrics` |
| MLflow | `http://PUBLIC_IP:5000` |
| JupyterLab | `http://PUBLIC_IP:8888` |
| Grafana | `http://PUBLIC_IP:30300` |
| Prometheus | `http://PUBLIC_IP:30090` |

## Commands

```bash
./scripts/configure-public-access.sh
./scripts/start-mlflow.sh
./scripts/expose-monitoring-public.sh
```

For Jupyter:

```bash
source .venv/bin/activate
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
```

For FastAPI:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## Important

Do not expose Kubernetes API `6443` to the Internet.

For a real deployment, use HTTPS, authentication, a reverse proxy/Ingress,
and source-IP restrictions.


## Kubernetes monitoring from public browser

After installing kube-prometheus-stack:

```bash
./scripts/setup-public-k8s-monitoring.sh
```

Then open:

```text
http://PUBLIC_IP:30300   # Grafana
http://PUBLIC_IP:30090   # Prometheus
```

For the full configuration see:

```text
KUBERNETES-PUBLIC-MONITORING.md
```
