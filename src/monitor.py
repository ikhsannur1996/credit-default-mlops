import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mlflow

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN = os.path.join(BASE, "data", "train.csv")
DB = os.path.join(BASE, "predictions.db")
REPORTS = os.path.join(BASE, "reports", "monitoring")
os.makedirs(REPORTS, exist_ok=True)

FEATURES = ["age", "income", "loan_amount", "tenure"]
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
mlflow.set_experiment("production-monitoring")

def psi(expected, actual, bins=10):
    expected = np.asarray(expected, dtype=float)
    actual = np.asarray(actual, dtype=float)
    cuts = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))
    if len(cuts) < 3:
        return 0.0
    e = np.histogram(expected, bins=cuts)[0] / len(expected)
    a = np.histogram(actual, bins=cuts)[0] / len(actual)
    e = np.clip(e, 1e-6, None)
    a = np.clip(a, 1e-6, None)
    return float(np.sum((a-e) * np.log(a/e)))

if not os.path.exists(DB):
    print("No predictions.db found. Make predictions first.")
    raise SystemExit(0)

train = pd.read_csv(TRAIN)
with sqlite3.connect(DB) as conn:
    prod = pd.read_sql_query("SELECT * FROM predictions", conn)

if len(prod) < 10:
    print("Need at least 10 predictions for monitoring.")
    raise SystemExit(0)

drifts = {f"psi_{f}": psi(train[f], prod[f]) for f in FEATURES}
max_psi = max(drifts.values())

with mlflow.start_run(run_name="production-monitoring"):
    mlflow.log_metrics({
        **drifts,
        "max_psi": max_psi,
        "prediction_count": len(prod),
        "default_prediction_rate": float(prod["prediction"].mean()),
        "average_probability": float(prod["probability"].mean()),
    })

    # Drift chart
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(drifts.keys(), drifts.values())
    ax.axhline(0.20, linestyle="--", label="PSI threshold")
    ax.set_title("Feature Drift - PSI")
    ax.set_ylabel("PSI")
    ax.legend()
    plt.xticks(rotation=30)
    fig.tight_layout()
    p = os.path.join(REPORTS, "feature_drift.png")
    fig.savefig(p); plt.close(fig)
    mlflow.log_artifact(p, "monitoring")

    # Prediction distribution
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(prod["probability"], bins=10)
    ax.set_title("Production Prediction Distribution")
    ax.set_xlabel("Default Probability")
    ax.set_ylabel("Count")
    fig.tight_layout()
    p = os.path.join(REPORTS, "production_prediction_distribution.png")
    fig.savefig(p); plt.close(fig)
    mlflow.log_artifact(p, "monitoring")

    status = "DRIFT" if max_psi > 0.20 else "OK"
    mlflow.set_tag("monitoring_status", status)

print("Monitoring complete.")
print(drifts)
print("STATUS:", status)
