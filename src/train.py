import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, f1_score

FEATURES = [
    "age", "income", "employment_years", "loan_amount",
    "loan_term", "interest_rate", "credit_score",
    "existing_loan", "monthly_installment", "debt_to_income",
    "credit_utilization", "number_of_accounts",
    "late_payment_count"
]

train = pd.read_csv("data/processed/train.csv")
val = pd.read_csv("data/processed/validation.csv")

model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("credit-default")

with mlflow.start_run() as run:
    model.fit(train[FEATURES], train.default)

    probability = model.predict_proba(val[FEATURES])[:, 1]
    prediction = (probability >= 0.5).astype(int)

    auc = roc_auc_score(val.default, probability)
    f1 = f1_score(val.default, prediction)

    mlflow.log_param("model", "logistic_regression")
    mlflow.log_metric("roc_auc", auc)
    mlflow.log_metric("f1", f1)
    mlflow.sklearn.log_model(model, "model")

    joblib.dump(model, "model/credit_default_model.joblib")

    print(f"run_id={run.info.run_id}")
    print(f"roc_auc={auc:.4f}")
    print(f"f1={f1:.4f}")
