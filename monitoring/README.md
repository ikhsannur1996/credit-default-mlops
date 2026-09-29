# Monitoring

Install kube-prometheus-stack:

```bash
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts

helm repo update

kubectl create namespace monitoring

helm install monitoring \
  prometheus-community/kube-prometheus-stack \
  -n monitoring
```

Grafana:

```bash
kubectl port-forward \
  -n monitoring \
  svc/monitoring-grafana 3000:80
```

Prometheus:

```bash
kubectl port-forward \
  -n monitoring \
  svc/monitoring-kube-prometheus-prometheus 9090:9090
```

API metrics:

```text
/metrics
```

Useful PromQL:

```promql
rate(credit_api_requests_total[5m])
```

```promql
rate(credit_predictions_total[5m])
```
