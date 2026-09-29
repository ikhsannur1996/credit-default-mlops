import numpy as np
import pandas as pd

def psi(reference, current, bins=10):
    edges = np.quantile(reference, np.linspace(0, 1, bins + 1))
    edges = np.unique(edges)
    if len(edges) < 3:
        return 0.0

    ref_count, _ = np.histogram(reference, bins=edges)
    cur_count, _ = np.histogram(current, bins=edges)

    ref_pct = ref_count / max(ref_count.sum(), 1)
    cur_pct = cur_count / max(cur_count.sum(), 1)

    eps = 1e-6
    ref_pct = np.clip(ref_pct, eps, None)
    cur_pct = np.clip(cur_pct, eps, None)

    return float(np.sum(
        (cur_pct - ref_pct) * np.log(cur_pct / ref_pct)
    ))

reference = pd.read_csv("data/processed/train.csv")
current = pd.read_csv("data/production_batch.csv")

for feature in [
    "credit_score",
    "income",
    "loan_amount",
    "debt_to_income",
    "credit_utilization",
]:
    score = psi(reference[feature], current[feature])
    print(f"{feature}: PSI={score:.4f}")
