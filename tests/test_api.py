from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict():
    payload = {
        "age": 45,
        "income": 6000000,
        "employment_years": 10,
        "loan_amount": 120000000,
        "loan_term": 36,
        "interest_rate": 15,
        "credit_score": 580,
        "existing_loan": 2,
        "monthly_installment": 4200000,
        "debt_to_income": 0.61,
        "credit_utilization": 0.82,
        "number_of_accounts": 5,
        "late_payment_count": 3
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "default_probability" in response.json()
