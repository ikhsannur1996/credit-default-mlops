# 05 - Monitoring

## Monitoring layers

This project focuses on ML monitoring rather than infrastructure monitoring.

### 1. Data drift

PSI is calculated for:

- age
- income
- loan_amount
- tenure

### 2. Prediction drift

The project records:

- default prediction rate
- average predicted probability
- prediction distribution

### 3. Data quality

The simple implementation can be extended with:

- missing values
- duplicates
- invalid ranges
- schema changes
- outliers

### 4. Model performance

The training/evaluation pipeline records:

- accuracy
- precision
- recall
- F1
- ROC-AUC
- PR-AUC

For true production performance monitoring, actual labels must become available after the business outcome occurs. Then a scheduled job can compare predictions with actual labels and log production performance to MLflow.

## What MLflow shows

The MLflow UI can be used to inspect:

```text
Runs
  |
  +-- Metrics
  +-- Parameters
  +-- Tags
  +-- Artifacts
  +-- Models
```

MLflow is not intended here to replace infrastructure monitoring such as CPU, memory, network, or Kubernetes monitoring.
