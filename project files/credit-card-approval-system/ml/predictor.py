import json, joblib, pandas as pd
from pathlib import Path
from ml.training import FEATURES, train
ROOT=Path(__file__).resolve().parents[1]

def ensure_model():
    path=ROOT/"models"/"best_model.pkl"
    if not path.exists(): train()
    return joblib.load(path)

def predict(payload):
    artifact=ensure_model(); frame=pd.DataFrame([{k:payload[k] for k in FEATURES}]); p=float(artifact["pipeline"].predict_proba(frame)[0,1]); approved=p>=.50
    risk="Low" if p>=.75 else "Medium" if p>=.5 else "High"
    drivers=[]
    if payload["payment_history"]>=80: drivers.append("Strong payment history")
    if payload["credit_history"]>=8: drivers.append("Established credit history")
    if payload["outstanding_debt"]>payload["annual_income"]*.35: drivers.append("High debt relative to income")
    if payload["credit_inquiries"]>=5: drivers.append("Frequent recent credit inquiries")
    if not drivers: drivers.append("Overall income, debt, and credit profile")
    return {"decision":"Approved" if approved else "Rejected","probability":round(p*100,2),"confidence":round(max(p,1-p)*100,2),"risk_level":risk,"key_features":drivers,"model_name":artifact["model_name"]}

def model_metrics():
    path=ROOT/"models"/"model_metrics.json"
    if not path.exists(): train()
    return json.loads(path.read_text())
