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


# PUBLIC IP ACCESS

This project is configured for a VM with a public IP. **Do not assume every
application should be exposed directly to the Internet**. For a personal lab,
you can expose selected ports through UFW and bind services to `0.0.0.0`.

## 1. Find the VM public IP

```bash
curl -4 ifconfig.me
```

Save it:

```bash
export PUBLIC_IP=$(curl -4 -s ifconfig.me)
echo $PUBLIC_IP
```

Also make sure your cloud/provider security group or network firewall allows
the ports you intend to use.

## 2. Configure Ubuntu firewall

Install UFW if needed:

```bash
sudo apt install -y ufw
```

Allow SSH first so you do not lock yourself out:

```bash
sudo ufw allow 22/tcp
```

For this lab, the application ports are:

| Service | Port | Public URL |
|---|---:|---|
| GitLab | 80 | `http://PUBLIC_IP/` |
| GitLab HTTPS | 443 | `https://PUBLIC_IP/` |
| JupyterLab | 8888 | `http://PUBLIC_IP:8888/` |
| MLflow | 5000 | `http://PUBLIC_IP:5000/` |
| FastAPI | 8000 | `http://PUBLIC_IP:8000/` |
| Prometheus | 9090 | `http://PUBLIC_IP:9090/` |
| Grafana | 3000 | `http://PUBLIC_IP:3000/` |
| Kubernetes API | 6443 | **Do not expose publicly** |

Open the lab ports:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3000/tcp
sudo ufw allow 5000/tcp
sudo ufw allow 8000/tcp
sudo ufw allow 8888/tcp
sudo ufw allow 9090/tcp
sudo ufw enable
sudo ufw status
```

**Important:** also open the same ports in your VM provider's firewall/security
group. UFW alone does not override a provider-level firewall.

## 3. Public FastAPI

Run directly:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Access:

```text
http://PUBLIC_IP:8000/docs
http://PUBLIC_IP:8000/health
http://PUBLIC_IP:8000/metrics
```

## 4. Public MLflow

The included `scripts/start-mlflow.sh` binds MLflow to localhost by default.
For public access, use:

```bash
mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri /opt/mlflow/mlruns \
  --default-artifact-root /opt/mlflow/artifacts
```

Access:

```text
http://PUBLIC_IP:5000
```

## 5. Public JupyterLab

Install:

```bash
source .venv/bin/activate
pip install jupyterlab
```

Start:

```bash
jupyter lab \
  --ip=0.0.0.0 \
  --port=8888 \
  --no-browser
```

Access:

```text
http://PUBLIC_IP:8888
```

Use the token printed by Jupyter.

## 6. Public Grafana

Instead of using `kubectl port-forward`, expose Grafana through a Kubernetes
NodePort.

Apply:

```bash
kubectl -n monitoring patch svc monitoring-grafana \
  -p '{"spec":{"type":"NodePort","ports":[{"name":"http-web","port":80,"targetPort":3000,"nodePort":30300}]}}'
```

Open:

```bash
sudo ufw allow 30300/tcp
```

Then:

```text
http://PUBLIC_IP:30300
```

Get the password:

```bash
kubectl get secret monitoring-grafana \
  -n monitoring \
  -o jsonpath="{.data.admin-password}" | base64 -d
echo
```

## 7. Public Prometheus

Expose Prometheus with NodePort:

```bash
kubectl -n monitoring patch svc monitoring-kube-prometheus-prometheus \
  -p '{"spec":{"type":"NodePort","ports":[{"name":"http-web","port":9090,"targetPort":9090,"nodePort":30090}]}}'
```

Open:

```bash
sudo ufw allow 30090/tcp
```

Access:

```text
http://PUBLIC_IP:30090
```

## 8. Public Kubernetes API

**Do not expose port 6443 to the public Internet for this personal lab.**

Keep:

```text
6443/tcp = private
```

The Kubernetes API is administrative infrastructure and should normally be
restricted to trusted IPs/VPN access.

## 9. GitLab on the same VM

For GitLab CE, map:

```text
80  → GitLab HTTP
443 → GitLab HTTPS
22  → GitLab SSH
```

Access:

```text
http://PUBLIC_IP/
```

If you want GitLab SSH from your laptop, make sure port 22 is available and
configure GitLab's SSH URL appropriately.

## 10. One-VM port map

```text
PUBLIC_IP
   │
   ├── :22     SSH
   ├── :80     GitLab
   ├── :443    GitLab HTTPS
   ├── :3000   Grafana
   ├── :5000   MLflow
   ├── :8000   FastAPI
   ├── :8888   JupyterLab
   ├── :9090   Prometheus
   ├── :30300  Grafana NodePort
   └── :30090  Prometheus NodePort
```

For Kubernetes services, NodePort is used because it is simple for a one-VM
lab. In a more production-like setup, use an Ingress/reverse proxy with TLS
instead of exposing many ports.

## 11. Provider firewall checklist

If your VM is on AWS, GCP, Azure, Oracle Cloud, DigitalOcean, etc., create
inbound rules for the ports you actually need.

Example:

```text
TCP 22     SSH
TCP 80     GitLab
TCP 443    GitLab HTTPS
TCP 3000   Grafana (if using direct access)
TCP 5000   MLflow
TCP 8000   FastAPI
TCP 8888   JupyterLab
TCP 9090   Prometheus
TCP 30300  Grafana NodePort
TCP 30090  Prometheus NodePort
```

Do **not** open `6443` publicly.

## 12. Security note

A public IP means these services are reachable from the Internet. Before
opening them:

- use strong passwords;
- keep Ubuntu and Docker updated;
- use Jupyter authentication/token;
- do not publish secrets in Git;
- restrict ports by source IP when possible;
- use HTTPS for real usage;
- do not expose Kubernetes API publicly;
- do not use default credentials;
- consider SSH tunneling/VPN for MLflow, Jupyter, and Prometheus instead of
  public exposure.

For a portfolio demo, exposing FastAPI and Grafana is usually enough. GitLab,
Jupyter, MLflow, and Prometheus can remain restricted if the goal is security
rather than demonstrating public access.


# KUBERNETES MONITORING FROM PUBLIC BROWSER

After installing the monitoring stack, run:

```bash
./scripts/setup-public-k8s-monitoring.sh
```

Then open:

```text
http://PUBLIC_IP:30300
```

for Grafana and:

```text
http://PUBLIC_IP:30090
```

for Prometheus.

The cloud/provider firewall must allow TCP `30300` and `30090`.

Do not expose Kubernetes API port `6443`.
