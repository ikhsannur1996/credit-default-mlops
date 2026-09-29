#!/usr/bin/env bash
set -e

kubectl -n monitoring patch svc monitoring-grafana \
  -p '{"spec":{"type":"NodePort","ports":[{"name":"http-web","port":80,"targetPort":3000,"nodePort":30300}]}}'

kubectl -n monitoring patch svc monitoring-kube-prometheus-prometheus \
  -p '{"spec":{"type":"NodePort","ports":[{"name":"http-web","port":9090,"targetPort":9090,"nodePort":30090}]}}'

echo "Grafana:     http://PUBLIC_IP:30300"
echo "Prometheus:  http://PUBLIC_IP:30090"
echo
kubectl get svc -n monitoring
