import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Run monitoring first.
subprocess.run([sys.executable, "src/monitor.py"], cwd=ROOT, check=True)

if os.getenv("AUTO_RETRAIN", "0") != "1":
    print("AUTO_RETRAIN is disabled.")
    print("Set AUTO_RETRAIN=1 to execute retraining.")
    raise SystemExit(0)

subprocess.run([sys.executable, "src/train.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "src/evaluate.py"], cwd=ROOT, check=True)

print("Retraining and evaluation complete. Check MLflow for the new run/model version.")
