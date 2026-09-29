# End-to-End MLOps with MLflow

A simple but complete MLOps portfolio project for credit-default prediction.

## Lifecycle

Data
→ Training
→ Evaluation
→ MLflow Tracking
→ Model Registry
→ FastAPI Serving
→ Prediction Logging
→ Production Monitoring
→ Drift Detection
→ Retraining

## MLflow is the central ML platform

MLflow stores:

- training parameters
- model metrics
- evaluation metrics
- model artifacts
- confusion matrix
- ROC curve
- Precision-Recall curve
- calibration curve
- threshold analysis
- feature importance
- prediction distribution
- data-quality metrics
- PSI / drift metrics
- monitoring charts
- registered model versions

## Monitoring coverage

### Model evaluation
- Accuracy
- Precision
- Recall
- F1
- ROC-AUC
- PR-AUC
- Confusion Matrix
- ROC Curve
- Precision-Recall Curve
- Calibration Curve
- Threshold Analysis
- Feature Importance
- Prediction Distribution

### Production monitoring
- Prediction volume
- Default prediction rate
- Feature missing rate
- Feature drift using PSI
- Prediction drift
- Production performance when labels are available
- Performance trend

## Run with Docker

```bash
docker compose up --build
```

Open:
- MLflow: http://localhost:5000
- FastAPI docs: http://localhost:8000/docs

## Important first step

Run training after MLflow is available:

```bash
python src/train.py
```

Then make predictions:

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"age":35,"income":10000000,"loan_amount":50000000,"tenure":24}'
```

Make at least 10 predictions before monitoring.

## Run evaluation manually

```bash
python src/evaluate.py
```

## Run monitoring

```bash
python src/monitor.py
```

## Retraining

```bash
AUTO_RETRAIN=1 python src/retrain.py
```

The retraining script checks drift and retrains when the configured threshold is exceeded.

## Local installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash scripts/start-mlflow.sh
```

In another terminal:

```bash
python src/train.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Public VM

For a simple VM deployment, expose:
- TCP 5000 for MLflow
- TCP 8000 for FastAPI

For real production, use HTTPS, authentication, secrets, a reverse proxy, and private storage.

## Architecture

```text
                  ┌───────────────┐
                  │   train.csv   │
                  └───────┬───────┘
                          ↓
                  ┌───────────────┐
                  │   train.py    │
                  └───────┬───────┘
                          ↓
                  ┌───────────────┐
                  │  evaluate.py  │
                  └───────┬───────┘
                          ↓
                  ┌───────────────┐
                  │    MLflow     │
                  │ Tracking      │
                  │ Evaluation    │
                  │ Registry      │
                  └───────┬───────┘
                          ↓
                  ┌───────────────┐
                  │    FastAPI    │
                  └───────┬───────┘
                          ↓
                    Predictions
                          ↓
                  ┌───────────────┐
                  │    SQLite     │
                  └───────┬───────┘
                          ↓
                  ┌───────────────┐
                  │   monitor.py  │
                  └───────┬───────┘
                          ↓
                    Drift / Quality
                          ↓
                  ┌───────────────┐
                  │  retrain.py   │
                  └───────┬───────┘
                          └────→ MLflow
```
