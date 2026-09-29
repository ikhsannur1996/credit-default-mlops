#!/usr/bin/env bash
set -e

echo "Exposing Grafana on NodePort 30300..."
kubectl -n monitoring patch svc monitoring-grafana \
  -p '{"spec":{"type":"NodePort","ports":[{"name":"http-web","port":80,"targetPort":3000,"nodePort":30300}]}}'

echo "Exposing Prometheus on NodePort 30090..."
kubectl -n monitoring patch svc monitoring-kube-prometheus-prometheus \
  -p '{"spec":{"type":"NodePort","ports":[{"name":"http-web","port":9090,"targetPort":9090,"nodePort":30090}]}}'

echo "Opening Ubuntu firewall ports..."
sudo ufw allow 30300/tcp
sudo ufw allow 30090/tcp

echo
echo "Monitoring services:"
kubectl get svc -n monitoring

echo
echo "Public IP:"
curl -4 -s ifconfig.me
echo

echo
echo "Grafana:    http://PUBLIC_IP:30300"
echo "Prometheus: http://PUBLIC_IP:30090"
echo
echo "Also configure TCP 30300 and 30090 in your cloud/provider firewall."
echo "Do NOT expose Kubernetes API port 6443."
