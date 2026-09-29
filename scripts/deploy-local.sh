#!/usr/bin/env bash
set -e

kubectl apply -f kubernetes/namespace.yaml

docker build -t credit-default-api:local .

docker save credit-default-api:local -o /tmp/credit-default-api.tar

sudo k3s ctr images import /tmp/credit-default-api.tar

kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

kubectl rollout status \
  deployment/credit-default-api \
  -n credit-default

kubectl get pods -n credit-default
