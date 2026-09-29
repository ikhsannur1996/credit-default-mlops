# 06 - Public Web Access

## Simple public access

For a learning/portfolio VM:

```text
http://PUBLIC_IP:5000
```

MLflow UI.

```text
http://PUBLIC_IP:8000/docs
```

FastAPI Swagger.

## Verify listening ports

On the server:

```bash
sudo ss -lntp | grep -E ':5000|:8000'
```

Docker:

```bash
docker compose ps
```

## Test from the server

```bash
curl http://localhost:5000
curl http://localhost:8000/health
```

## Test from your laptop

```bash
curl http://PUBLIC_IP:8000/health
```

## Cloud firewall

The VM firewall and cloud security group are separate controls.

You may need both:

```text
Ubuntu UFW
+
Cloud firewall/security group
```

Open TCP 5000 and 8000 for the demo.

## Production recommendation

Do not expose MLflow and FastAPI directly on high ports in a real production environment.

Preferred:

```text
Internet
   |
 HTTPS 443
   |
Nginx / Caddy
   |
   +---- MLflow
   |
   +---- FastAPI
```

Use:

- HTTPS
- authentication
- restricted firewall rules
- secrets management
- backups
- private MLflow storage

The simple project intentionally keeps this out to avoid unnecessary complexity.
