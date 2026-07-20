# CreditFlow — Automated Credit Card Approval System

CreditFlow is a complete Flask and scikit-learn demonstration system for secure credit-card applications, real-time model scoring, saved prediction history, model comparison, and administrator review.

> The included data generator is for demonstration. Do not use it, or this project as-is, to make real lending decisions. Production lending requires approved data, fairness testing, governance, human oversight, legal review, monitoring, and security controls.

## Demo video

Demo video: https://drive.google.com/file/d/1skVcN0LgVLmPoJVEtt6i6fnB4o1ZgwWR/view?usp=sharing

## Quick start

```bash
cd credit-card-approval-system
python -m venv .venv
pip install -r requirements.txt
python -m ml.training
python app.py
```

On Windows activate with `.venv\\Scripts\\activate`; on macOS/Linux use `source .venv/bin/activate`. Open `http://127.0.0.1:5000`. The seeded administrative identity is `admin@example.com` / `Admin123!`; change it immediately for any non-demo use.

## Training and evaluation

Place a labelled CSV at `dataset/credit_applications.csv` to train on your own data. It must contain the fields declared in `ml/training.py` plus binary `approved`. If absent, training generates reproducible demo data. The pipeline removes duplicates, imputes missing values, one-hot encodes categories, scales numeric values, runs a stratified split and four-fold cross-validation, then compares Logistic Regression, Decision Tree, Random Forest, and Gradient Boosting. It reports accuracy, precision, recall, F1, ROC-AUC, and a confusion matrix in `models/model_metrics.json`, selecting the highest ROC-AUC model for `models/best_model.pkl`.

For EDA, use the training dataset to create histograms (distributions), count plots (category balance), box plots (outliers), pair/scatter plots (relationships), a heatmap (numeric correlation), distribution plots (class separation), and feature importance charts (model driver checks). Perform these visual checks on each approved data refresh.

## Deployment

Build the container with `docker build -t creditflow .`, then run `docker run -p 5000:5000 -e SECRET_KEY="a-long-random-secret" creditflow`. See [ERD](docs/ERD.md), [architecture](docs/ARCHITECTURE.md), and [Watson guide](deployment/DEPLOYMENT.md).

Production setup should use a managed database, HTTPS, a securely stored `SECRET_KEY`, a configured email provider for password resets, audit logging, access control, monitoring, and validated regulatory model governance.
