# 04 - MLflow Configuration and Usage

## MLflow responsibilities

MLflow is the central ML platform in this project.

It handles:

1. Experiment tracking
2. Metrics
3. Parameters
4. Model artifacts
5. Model Registry
6. Evaluation artifacts
7. Monitoring metrics
8. Drift metrics

## Training metrics

The training run logs:

```text
accuracy
precision
recall
f1
roc_auc
pr_auc
```

## Evaluation artifacts

The evaluation run creates:

```text
evaluation/
├── confusion_matrix.png
├── roc_curve.png
├── precision_recall_curve.png
├── calibration_curve.png
├── feature_importance.png
├── prediction_distribution.png
├── threshold_analysis.png
└── threshold_analysis.csv
```

These appear under the MLflow run's Artifacts section.

## Monitoring artifacts

Monitoring creates:

```text
monitoring/
├── feature_drift.png
└── production_prediction_distribution.png
```

## Drift metrics

The monitoring script logs:

```text
psi_age
psi_income
psi_loan_amount
psi_tenure
max_psi
```

The demo threshold is:

```text
PSI <= 0.20  -> OK
PSI > 0.20   -> DRIFT
```

This threshold is illustrative. Production thresholds should be validated for the actual business/model.

## Model Registry

Training registers:

```text
credit-default
```

FastAPI reads the latest registered version.

For a stricter production workflow, change this to an explicit production alias such as:

```text
champion
```

and deploy only approved versions.
