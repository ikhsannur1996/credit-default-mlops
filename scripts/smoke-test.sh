#!/usr/bin/env bash
set -e

echo "== Files =="
test -f data/raw/credit_default.csv
test -f data/processed/train.csv
test -f data/processed/validation.csv
test -f data/processed/test.csv
test -f model/credit_default_model.joblib

echo "== Kubernetes =="
kubectl get deployment credit-default-api -n credit-default

echo "== Pods =="
kubectl get pods -n credit-default

echo "Smoke test passed."
