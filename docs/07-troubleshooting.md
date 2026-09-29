# 07 - Troubleshooting

## Container status

```bash
docker compose ps
```

## Logs

MLflow:

```bash
docker compose logs -f mlflow
```

API:

```bash
docker compose logs -f api
```

## Restart

```bash
docker compose restart
```

Full rebuild:

```bash
docker compose down
docker compose up -d --build
```

## Port already in use

Check:

```bash
sudo ss -lntp | grep ':5000'
sudo ss -lntp | grep ':8000'
```

Change host ports in `docker-compose.yml`.

## MLflow has no experiments

Run:

```bash
docker compose exec api python src/train.py
```

Then refresh MLflow.

## API says no registered model

Run:

```bash
docker compose exec api python src/train.py
```

Then test `/health` and `/predict`.

## Monitoring says not enough predictions

Make at least 10 calls to `/predict`.

## Browser cannot access the VM

Check:

```bash
docker compose ps
sudo ufw status
sudo ss -lntp
```

Then check the cloud provider security group/firewall.

## Check public IP

```bash
curl -4 ifconfig.me
```

## Stop everything

```bash
docker compose down
```

Data is persisted through the project directory because the compose file mounts the project into the containers.
