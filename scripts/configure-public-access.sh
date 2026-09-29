#!/usr/bin/env bash
set -e

echo "Configuring UFW for the one-VM public MLOps lab..."

sudo apt-get update
sudo apt-get install -y ufw

# Always allow SSH before enabling UFW.
sudo ufw allow 22/tcp

for port in 80 443 3000 5000 8000 8888 9090 30300 30090; do
  sudo ufw allow "${port}/tcp"
done

sudo ufw --force enable

echo
echo "UFW status:"
sudo ufw status verbose

echo
echo "Public IP:"
curl -4 -s ifconfig.me || true
echo
echo
echo "Remember to add the same inbound rules in your VM provider firewall/security group."
echo "Do NOT open Kubernetes API port 6443 publicly."
