# Public VM Quick Start

## 1. Install
Read `docs/01-installation.md`.

## 2. Configure
Read `docs/02-configuration.md`.

## 3. Start
```bash
docker compose up -d --build
```

## 4. Train
```bash
docker compose exec api python src/train.py
docker compose exec api python src/evaluate.py
```

## 5. Browser
```text
http://PUBLIC_IP:5000
http://PUBLIC_IP:8000/docs
```

## 6. Generate predictions
Use Swagger `/predict`.

## 7. Monitor
```bash
docker compose exec api python src/monitor.py
```

## 8. Retrain
```bash
docker compose exec -e AUTO_RETRAIN=1 api python src/retrain.py
```

For detailed configuration, firewall, public access, MLflow, monitoring, and troubleshooting, read the files in `docs/`.
