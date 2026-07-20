"""Reproducible training pipeline. Uses dataset/credit_applications.csv if present;
otherwise generates realistic, labelled demonstration data for a working local app."""
import json
from pathlib import Path
import joblib, numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["age","gender","annual_income","employment_type","employment_duration","education","marital_status","existing_loan_amount","credit_inquiries","credit_history","monthly_income","outstanding_debt","payment_history","housing_type","occupation"]
NUMERIC = [x for x in FEATURES if x not in ["gender","employment_type","education","marital_status","housing_type","occupation"]]
CATEGORICAL = [x for x in FEATURES if x not in NUMERIC]

def synthetic_data(n=1600, seed=42):
    r = np.random.default_rng(seed)
    df = pd.DataFrame({"age":r.integers(21,70,n), "gender":r.choice(["Female","Male","Other"],n), "annual_income":r.lognormal(11.1,.55,n).clip(15000,300000), "employment_type":r.choice(["Salaried","Self-employed","Business","Unemployed"],n,p=[.55,.2,.18,.07]), "employment_duration":r.uniform(0,30,n), "education":r.choice(["High School","Bachelor","Master","Doctorate"],n,p=[.2,.47,.25,.08]), "marital_status":r.choice(["Single","Married","Divorced"],n,p=[.4,.5,.1]), "existing_loan_amount":r.gamma(2,7000,n), "credit_inquiries":r.integers(0,9,n), "credit_history":r.uniform(0,25,n), "monthly_income":0., "outstanding_debt":r.gamma(2,5000,n), "payment_history":r.uniform(35,100,n), "housing_type":r.choice(["Own","Rent","Mortgage"],n,p=[.37,.35,.28]), "occupation":r.choice(["Professional","Manager","Clerical","Service","Technician","Student"],n)})
    df["monthly_income"] = df.annual_income / 12
    score = -2.2 + .000017*df.annual_income - .000025*df.existing_loan_amount - .00003*df.outstanding_debt + .055*df.credit_history + .038*df.payment_history - .16*df.credit_inquiries + .55*(df.employment_type=="Salaried") + .4*(df.housing_type=="Own")
    p = 1/(1+np.exp(-score)); df["approved"] = r.binomial(1,p)
    return df

def _pipeline(model):
    prep=ColumnTransformer([( "num",Pipeline([( "impute",SimpleImputer(strategy="median")),("scale",StandardScaler())]),NUMERIC),("cat",Pipeline([( "impute",SimpleImputer(strategy="most_frequent")),("encode",OneHotEncoder(handle_unknown="ignore"))]),CATEGORICAL)])
    return Pipeline([("preprocessor",prep),("model",model)])

def train():
    source=ROOT/"dataset"/"credit_applications.csv"; df=pd.read_csv(source) if source.exists() else synthetic_data()
    df=df.drop_duplicates().dropna(subset=["approved"]); X,y=df[FEATURES],df["approved"].astype(int)
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,stratify=y,random_state=42)
    candidates={"Logistic Regression":LogisticRegression(max_iter=1500,class_weight="balanced"),"Decision Tree":DecisionTreeClassifier(max_depth=7,min_samples_leaf=12,random_state=42,class_weight="balanced"),"Random Forest":RandomForestClassifier(n_estimators=300,min_samples_leaf=5,random_state=42,class_weight="balanced",n_jobs=-1),"XGBoost (Gradient Boosting)":GradientBoostingClassifier(n_estimators=150,max_depth=3,learning_rate=.05,random_state=42)}
    metrics={}; fitted={}
    for name,model in candidates.items():
        pipe=_pipeline(model); pipe.fit(Xtr,ytr); pred=pipe.predict(Xte); proba=pipe.predict_proba(Xte)[:,1]
        metrics[name]={"accuracy":round(accuracy_score(yte,pred),4),"precision":round(precision_score(yte,pred,zero_division=0),4),"recall":round(recall_score(yte,pred,zero_division=0),4),"f1":round(f1_score(yte,pred,zero_division=0),4),"roc_auc":round(roc_auc_score(yte,proba),4),"confusion_matrix":confusion_matrix(yte,pred).tolist(),"cv_roc_auc":round(cross_val_score(pipe,X,y,cv=StratifiedKFold(4,shuffle=True,random_state=42),scoring="roc_auc").mean(),4)}; fitted[name]=pipe
    best=max(metrics,key=lambda k:metrics[k]["roc_auc"]); artifact={"pipeline":fitted[best],"model_name":best,"features":FEATURES}
    (ROOT/"models").mkdir(exist_ok=True); joblib.dump(artifact,ROOT/"models"/"best_model.pkl")
    (ROOT/"models"/"model_metrics.json").write_text(json.dumps({"best_model":best,"models":metrics},indent=2))
    return best,metrics

if __name__ == "__main__":
    best,metrics=train(); print(f"Saved {best} with ROC-AUC {metrics[best]['roc_auc']}")
