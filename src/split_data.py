import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/raw/credit_default.csv")

train, temp = train_test_split(
    df, test_size=0.30, stratify=df.default, random_state=42
)

validation, test = train_test_split(
    temp, test_size=0.50, stratify=temp.default, random_state=42
)

Path("data/processed").mkdir(parents=True, exist_ok=True)

train.to_csv("data/processed/train.csv", index=False)
validation.to_csv("data/processed/validation.csv", index=False)
test.to_csv("data/processed/test.csv", index=False)

print(f"train={len(train)} validation={len(validation)} test={len(test)}")
