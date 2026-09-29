import os
import joblib
import pandas as pd

from fastapi import FastAPI, Request
from prometheus_client import Counter, make_asgi_app
from pydantic import BaseModel

MODEL_PATH = os.getenv("MODEL_PATH", "model/credit_default_model.joblib")
model = joblib.load(MODEL_PATH)

app = FastAPI(title="Credit Default API")

REQUESTS = Counter(
    "credit_api_requests_total",
    "Total API requests"
)

PREDICTIONS = Counter(
    "credit_predictions_total",
    "Total predictions"
)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

class CreditRequest(BaseModel):
    age: int
    income: float
    employment_years: float
    loan_amount: float
    loan_term: int
    interest_rate: float
    credit_score: int
    existing_loan: int
    monthly_installment: float
    debt_to_income: float
    credit_utilization: float
    number_of_accounts: int
    late_payment_count: int

@app.middleware("http")
async def count_requests(request: Request, call_next):
    REQUESTS.inc()
    return await call_next(request)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict")
def predict(request: CreditRequest):
    df = pd.DataFrame([request.model_dump()])
    probability = float(model.predict_proba(df)[:, 1][0])
    prediction = int(probability >= 0.5)

    PREDICTIONS.inc()

    return {
        "prediction": prediction,
        "default_probability": round(probability, 6)
    }
