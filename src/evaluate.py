import joblib
import pandas as pd
from sklearn.metrics import roc_auc_score, classification_report

FEATURES = [
    "age", "income", "employment_years", "loan_amount",
    "loan_term", "interest_rate", "credit_score",
    "existing_loan", "monthly_installment", "debt_to_income",
    "credit_utilization", "number_of_accounts",
    "late_payment_count"
]

test = pd.read_csv("data/processed/test.csv")
model = joblib.load("model/credit_default_model.joblib")

prob = model.predict_proba(test[FEATURES])[:, 1]
pred = (prob >= 0.5).astype(int)

print("ROC-AUC:", round(roc_auc_score(test.default, prob), 4))
print(classification_report(test.default, pred))
