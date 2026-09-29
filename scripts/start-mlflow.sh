#!/usr/bin/env bash
set -e

mkdir -p /opt/mlflow/mlruns /opt/mlflow/artifacts

nohup mlflow server \
  --host 127.0.0.1 \
  --port 5000 \
  --backend-store-uri /opt/mlflow/mlruns \
  --default-artifact-root /opt/mlflow/artifacts \
  > /opt/mlflow/mlflow.log 2>&1 &

echo "MLflow started on 127.0.0.1:5000"
