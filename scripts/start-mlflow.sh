#!/usr/bin/env bash
set -e

mkdir -p /opt/mlflow/mlruns /opt/mlflow/artifacts

pkill -f "mlflow server.*--port 5000" 2>/dev/null || true

nohup mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri /opt/mlflow/mlruns \
  --default-artifact-root /opt/mlflow/artifacts \
  > /opt/mlflow/mlflow.log 2>&1 &

echo "MLflow started on 0.0.0.0:5000"
echo "WARNING: port 5000 is now Internet-accessible if the VM/provider firewall allows it."
