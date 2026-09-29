import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    ConfusionMatrixDisplay, roc_curve, precision_recall_curve,
    calibration_curve
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data", "train.csv")
REPORTS = os.path.join(BASE, "reports", "evaluation")
os.makedirs(REPORTS, exist_ok=True)

FEATURES = ["age", "income", "loan_amount", "tenure"]

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
mlflow.set_experiment("credit-default-evaluation")

df = pd.read_csv(DATA)
X_train, X_test, y_train, y_test = train_test_split(
    df[FEATURES], df["default"], test_size=0.25, random_state=42, stratify=df["default"]
)

model = RandomForestClassifier(n_estimators=150, max_depth=6, random_state=42)
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

with mlflow.start_run(run_name="detailed-evaluation"):
    mlflow.log_metrics(metrics)

    # 1. Confusion matrix
    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay(confusion_matrix(y_test, pred)).plot(ax=ax)
    ax.set_title("Confusion Matrix")
    fig.tight_layout()
    p = os.path.join(REPORTS, "confusion_matrix.png")
    fig.savefig(p); plt.close(fig)
    mlflow.log_artifact(p, "evaluation")

    # 2. ROC curve
    fpr, tpr, _ = roc_curve(y_test, prob)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(fpr, tpr, label=f"AUC={metrics['roc_auc']:.3f}")
    ax.plot([0, 1], [0, 1], linestyle="--")
    ax.set_title("ROC Curve"); ax.set_xlabel("False Positive Rate"); ax.set_ylabel("True Positive Rate")
    ax.legend(); fig.tight_layout()
    p = os.path.join(REPORTS, "roc_curve.png")
    fig.savefig(p); plt.close(fig)
    mlflow.log_artifact(p, "evaluation")

    # 3. Precision-Recall curve
    precision, recall, _ = precision_recall_curve(y_test, prob)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(recall, precision, label=f"PR-AUC={metrics['pr_auc']:.3f}")
    ax.set_title("Precision-Recall Curve"); ax.set_xlabel("Recall"); ax.set_ylabel("Precision")
    ax.legend(); fig.tight_layout()
    p = os.path.join(REPORTS, "precision_recall_curve.png")
    fig.savefig(p); plt.close(fig)
    mlflow.log_artifact(p, "evaluation")

    # 4. Calibration curve
    frac_pos, mean_pred = calibration_curve(y_test, prob, n_bins=5)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(mean_pred, frac_pos, marker="o", label="Model")
    ax.plot([0, 1], [0, 1], linestyle="--", label="Perfect calibration")
    ax.set_title("Calibration Curve"); ax.set_xlabel("Mean Predicted Probability"); ax.set_ylabel("Fraction Positive")
    ax.legend(); fig.tight_layout()
    p = os.path.join(REPORTS, "calibration_curve.png")
    fig.savefig(p); plt.close(fig)
    mlflow.log_artifact(p, "evaluation")

    # 5. Feature importance
    importance = pd.Series(model.feature_importances_, index=FEATURES).sort_values()
    fig, ax = plt.subplots(figsize=(7, 4))
    importance.plot(kind="barh", ax=ax)
    ax.set_title("Feature Importance")
    fig.tight_layout()
    p = os.path.join(REPORTS, "feature_importance.png")
    fig.savefig(p); plt.close(fig)
    mlflow.log_artifact(p, "evaluation")

    # 6. Prediction distribution
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(prob, bins=10)
    ax.set_title("Prediction Probability Distribution")
    ax.set_xlabel("Default Probability"); ax.set_ylabel("Count")
    fig.tight_layout()
    p = os.path.join(REPORTS, "prediction_distribution.png")
    fig.savefig(p); plt.close(fig)
    mlflow.log_artifact(p, "evaluation")

    # 7. Threshold analysis
    rows = []
    for threshold in np.arange(0.1, 0.91, 0.1):
        p2 = (prob >= threshold).astype(int)
        rows.append({
            "threshold": round(float(threshold), 2),
            "precision": precision_score(y_test, p2, zero_division=0),
            "recall": recall_score(y_test, p2, zero_division=0),
            "f1": f1_score(y_test, p2, zero_division=0),
        })
    threshold_df = pd.DataFrame(rows)
    threshold_df.to_csv(os.path.join(REPORTS, "threshold_analysis.csv"), index=False)
    mlflow.log_artifact(os.path.join(REPORTS, "threshold_analysis.csv"), "evaluation")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(threshold_df["threshold"], threshold_df["precision"], marker="o", label="Precision")
    ax.plot(threshold_df["threshold"], threshold_df["recall"], marker="o", label="Recall")
    ax.plot(threshold_df["threshold"], threshold_df["f1"], marker="o", label="F1")
    ax.set_title("Threshold Analysis"); ax.set_xlabel("Threshold"); ax.set_ylabel("Score")
    ax.legend(); fig.tight_layout()
    p = os.path.join(REPORTS, "threshold_analysis.png")
    fig.savefig(p); plt.close(fig)
    mlflow.log_artifact(p, "evaluation")

    print("Detailed evaluation logged to MLflow.")
