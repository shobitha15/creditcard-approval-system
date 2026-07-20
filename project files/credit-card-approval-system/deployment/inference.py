"""IBM Watson Machine Learning-compatible scoring entry point."""
import joblib, pandas as pd
MODEL = None
def load_model():
    global MODEL
    if MODEL is None: MODEL=joblib.load("models/best_model.pkl")
    return MODEL
def score(payload):
    model=load_model(); fields=payload["input_data"][0]["fields"]; values=payload["input_data"][0]["values"]
    frame=pd.DataFrame(values,columns=fields); probabilities=model["pipeline"].predict_proba(frame)[:,1]
    return {"predictions":[{"fields":["approved_probability","decision"],"values":[[float(p),"Approved" if p>=.5 else "Rejected"] for p in probabilities]}]}
