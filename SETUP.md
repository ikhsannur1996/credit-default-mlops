# SETUP — One VM

## Recommended VM

- Ubuntu Server 24.04 LTS
- 4 vCPU
- 16 GB RAM
- 100 GB disk
- Static/private IP

## 1. Install base packages

```bash
sudo apt update
sudo apt upgrade -y

sudo apt install -y \
  git curl wget unzip zip jq tree \
  python3 python3-venv python3-pip
```

## 2. Install Docker

```bash
sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc

sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

sudo apt install -y \
  docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin

sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

Logout/login again.

Test:

```bash
docker run --rm hello-world
```

## 3. Install project

```bash
sudo mkdir -p /opt/credit-default-mlops
sudo chown -R $USER:$USER /opt/credit-default-mlops
cd /opt/credit-default-mlops
```

Copy this repository here.

## 4. Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Generate data

```bash
python src/generate_data.py
python src/validate_data.py
python src/split_data.py
```

## 6. Start MLflow

```bash
./scripts/start-mlflow.sh
```

Use SSH tunnel from your laptop:

```bash
ssh -L 5000:127.0.0.1:5000 USER@VM_IP
```

Open:

```text
http://localhost:5000
```

## 7. Train

```bash
source .venv/bin/activate
python src/train.py
python src/evaluate.py
```

## 8. Test API locally

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Then:

```bash
curl http://127.0.0.1:8000/health
```

## 9. Build API image

```bash
docker build -t credit-default-api:local .
```

## 10. Install k3s

```bash
curl -sfL https://get.k3s.io | sh -
```

Test:

```bash
sudo k3s kubectl get nodes
```

## 11. Deploy

```bash
./scripts/deploy-local.sh
```

Check:

```bash
kubectl get pods -n credit-default
```

## 12. Test Kubernetes API

```bash
kubectl port-forward \
  -n credit-default \
  svc/credit-default-api 8000:8000
```

Then:

```bash
curl http://127.0.0.1:8000/health
```

## 13. Monitoring

Install Helm:

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Install Prometheus/Grafana:

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

Open:

```text
http://localhost:3000
```

Get password:

```bash
kubectl get secret monitoring-grafana \
  -n monitoring \
  -o jsonpath="{.data.admin-password}" | base64 -d
echo
```

## 14. Drift demo

```bash
python src/generate_drift.py
python src/drift.py
```

## 15. GitLab

GitLab is intentionally kept separate from the application Docker Compose.

Use GitLab CE on the same VM and create a repository containing this project.

For a small personal VM, start GitLab with Docker and persistent volumes. Then install/register GitLab Runner.

## 16. Final test

```bash
./scripts/smoke-test.sh
```

Expected:

```text
data OK
model OK
API OK
Kubernetes OK
```
