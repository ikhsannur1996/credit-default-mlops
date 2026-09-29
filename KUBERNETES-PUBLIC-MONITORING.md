# Kubernetes Monitoring via Public Web

This project uses **Grafana + Prometheus** to monitor the k3s Kubernetes cluster
from a browser through the VM public IP.

## Architecture

```text
Internet
   |
   v
PUBLIC IP
   |
   +---- :30300 ----> Grafana
   |                    |
   |                    v
   |                Prometheus
   |                    |
   |                    v
   |                   k3s
   |
   +---- :30090 ----> Prometheus Web UI
```

## 1. Install monitoring stack

```bash
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts

helm repo update

kubectl create namespace monitoring

helm install monitoring \
  prometheus-community/kube-prometheus-stack \
  -n monitoring
```

Check:

```bash
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

Wait until the pods are Running.

## 2. Expose Grafana through NodePort

Run:

```bash
kubectl -n monitoring patch svc monitoring-grafana \
  -p '{"spec":{"type":"NodePort","ports":[{"name":"http-web","port":80,"targetPort":3000,"nodePort":30300}]}}'
```

Check:

```bash
kubectl get svc monitoring-grafana -n monitoring
```

Expected NodePort:

```text
30300
```

## 3. Expose Prometheus Web UI

Run:

```bash
kubectl -n monitoring patch svc monitoring-kube-prometheus-prometheus \
  -p '{"spec":{"type":"NodePort","ports":[{"name":"http-web","port":9090,"targetPort":9090,"nodePort":30090}]}}'
```

Check:

```bash
kubectl get svc \
  monitoring-kube-prometheus-prometheus \
  -n monitoring
```

Expected NodePort:

```text
30090
```

## 4. Open Ubuntu firewall

```bash
sudo ufw allow 30300/tcp
sudo ufw allow 30090/tcp
sudo ufw status
```

## 5. Open provider firewall

Your VM provider must also allow:

```text
TCP 30300
TCP 30090
```

For example, in a cloud security group/inbound-rule page:

```text
Protocol: TCP
Port: 30300
Source: your IP (recommended)
```

and:

```text
Protocol: TCP
Port: 30090
Source: your IP (recommended)
```

For a public demo you can use:

```text
Source: 0.0.0.0/0
```

but this exposes the monitoring interfaces to the Internet.

## 6. Access Grafana

Get the VM public IP:

```bash
curl -4 ifconfig.me
```

Then open:

```text
http://PUBLIC_IP:30300
```

Example:

```text
http://103.xxx.xxx.xxx:30300
```

Get the initial Grafana password:

```bash
kubectl get secret monitoring-grafana \
  -n monitoring \
  -o jsonpath="{.data.admin-password}" | base64 -d
echo
```

Username:

```text
admin
```

## 7. Access Prometheus

Open:

```text
http://PUBLIC_IP:30090
```

Prometheus should already be connected to the kube-prometheus-stack metrics
components.

## 8. Kubernetes metrics

Grafana can monitor:

### Cluster

- Cluster CPU
- Cluster memory
- Node count
- Pod count
- Namespace count

### Node

- CPU utilization
- Memory utilization
- Disk usage
- Network traffic
- Node status

### Pod

- CPU
- Memory
- Restart count
- Running status
- Container status

### Deployment

- Desired replicas
- Available replicas
- Unavailable replicas
- Replica health

### API

The Credit Default API also exposes:

```text
/metrics
```

Example:

```text
http://PUBLIC_IP:8000/metrics
```

Prometheus can scrape these application metrics when the API is configured
for scraping.

## 9. Recommended dashboard

Create a Grafana dashboard called:

```text
Credit Default MLOps
```

Recommended panels:

```text
┌─────────────────────────────────────────────┐
│ CREDIT DEFAULT MLOps                        │
├──────────────┬──────────────┬───────────────┤
│ Nodes        │ Pods         │ API Status    │
│ 1            │ 2            │ UP            │
├──────────────┴──────────────┴───────────────┤
│ Kubernetes CPU Usage                         │
│ █████████████░░░░░                          │
├─────────────────────────────────────────────┤
│ Kubernetes Memory Usage                      │
│ ████████░░░░░░░                             │
├──────────────────────┬──────────────────────┤
│ Pod Restarts         │ API Requests         │
│ 0                    │ 125/min              │
├──────────────────────┼──────────────────────┤
│ Predictions          │ Deployment Ready     │
│ 42/min               │ 2/2                  │
└──────────────────────┴──────────────────────┘
```

## 10. Useful PromQL

CPU:

```promql
sum(rate(container_cpu_usage_seconds_total[5m]))
```

Memory:

```promql
sum(container_memory_working_set_bytes)
```

Pod restarts:

```promql
sum(kube_pod_container_status_restarts_total)
```

Available replicas:

```promql
sum(kube_deployment_status_replicas_available)
```

API requests:

```promql
rate(credit_api_requests_total[5m])
```

Predictions:

```promql
rate(credit_predictions_total[5m])
```

## 11. Security recommendation

For a personal portfolio/demo:

```text
Public
  |
  +--> Grafana :30300
  |
  +--> FastAPI :8000
```

Keep these restricted where possible:

```text
Prometheus :30090
Jupyter :8888
MLflow :5000
GitLab
Kubernetes API :6443
```

Most importantly:

```text
DO NOT expose Kubernetes API :6443 publicly.
```

For a stronger setup, restrict monitoring ports to your own public IP in
the cloud firewall:

```text
Your IP --> VM:30300
Your IP --> VM:30090
```

## 12. Verify everything

```bash
kubectl get nodes
kubectl get pods -A
kubectl get svc -A
```

Then from your laptop browser:

```text
http://PUBLIC_IP:30300
http://PUBLIC_IP:30090
http://PUBLIC_IP:8000/docs
```

At this point Kubernetes, Prometheus, Grafana, and the ML API are accessible
from the public browser.
