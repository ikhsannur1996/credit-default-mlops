import os
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data", "train.csv")
FEATURES = ["age", "income", "loan_amount", "tenure"]

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
mlflow.set_experiment("credit-default")

df = pd.read_csv(DATA)
X_train, X_test, y_train, y_test = train_test_split(
    df[FEATURES], df["default"], test_size=0.25, random_state=42, stratify=df["default"]
)

model = RandomForestClassifier(
    n_estimators=150, max_depth=6, random_state=42
)

with mlflow.start_run(run_name="training"):
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "pr_auc": average_precision_score(y_test, prob),
    }

    mlflow.log_params({
        "model": "RandomForestClassifier",
        "n_estimators": 150,
        "max_depth": 6,
        "random_state": 42,
        "feature_count": len(FEATURES),
    })
    mlflow.log_metrics(metrics)

    mlflow.sklearn.log_model(
        model,
        name="credit_default_model",
        registered_model_name="credit-default"
    )

    print("Training metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")
