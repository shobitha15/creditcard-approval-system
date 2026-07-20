# System architecture

```mermaid
flowchart LR
Browser --> Flask[Flask routes]
Flask --> Auth[Flask-Login]
Flask --> Predictor[Joblib prediction pipeline]
Flask --> DB[(SQLite / SQLAlchemy)]
Training[ml/training.py] --> Model[models/best_model.pkl]
Model --> Predictor
```

The training pipeline cleans duplicate rows, uses median/most-frequent imputation, one-hot encodes categories, scales numeric features, performs stratified splitting and cross-validation, compares four classifiers, and saves the best ROC-AUC artifact.
