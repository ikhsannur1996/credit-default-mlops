# Quick Demo

Run the same pipeline from terminal:

```bash
source .venv/bin/activate

python src/generate_data.py
python src/validate_data.py
python src/split_data.py

# Start MLflow first:
./scripts/start-mlflow.sh

python src/train.py
python src/evaluate.py

uvicorn api.main:app --host 0.0.0.0 --port 8000
```

JupyterLab can be used for EDA, experiments, and visualizations.
