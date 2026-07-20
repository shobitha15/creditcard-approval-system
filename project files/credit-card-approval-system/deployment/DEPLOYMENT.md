# IBM Watson Machine Learning deployment

1. Train locally: `python -m ml.training`.
2. Create a Watson Machine Learning service and project in IBM Cloud.
3. Upload `models/best_model.pkl`, `deployment/inference.py`, and `watson_deployment.json` as the model asset/package.
4. Create an online deployment using the Python 3.11 runtime.

Send all fifteen model feature fields, in training order, through the `input_data` payload handled by `inference.py`. Configure IBM Cloud Secrets, TLS, access controls, monitoring, and approved model governance before processing real applicant data.
