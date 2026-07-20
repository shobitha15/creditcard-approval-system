from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from services.database import db, CreditApplication, PredictionHistory
from ml.predictor import predict
application_bp=Blueprint("application",__name__)
FIELDS={"age":int,"gender":str,"annual_income":float,"employment_type":str,"employment_duration":float,"education":str,"marital_status":str,"existing_loan_amount":float,"credit_inquiries":int,"credit_history":float,"monthly_income":float,"outstanding_debt":float,"payment_history":float,"housing_type":str,"occupation":str}
@application_bp.route("/dashboard")
@login_required
def dashboard():
    apps=CreditApplication.query.filter_by(user_id=current_user.id).order_by(CreditApplication.submitted_at.desc()).all()
    approved=sum(a.prediction and a.prediction.decision=="Approved" for a in apps)
    return render_template("dashboard.html",apps=apps,total=len(apps),approved=approved)
@application_bp.route("/apply",methods=["GET","POST"])
@login_required
def apply():
    if request.method=="POST":
        try:
            data={key:converter(request.form[key].strip()) for key,converter in FIELDS.items()}
            if not 18<=data["age"]<=100 or data["annual_income"]<=0 or data["monthly_income"]<=0 or not 0<=data["payment_history"]<=100 or min(data["employment_duration"],data["credit_history"],data["existing_loan_amount"],data["outstanding_debt"])<0: raise ValueError
        except (KeyError,ValueError): flash("Please provide valid values. Age, amounts, and history fields cannot be negative.","danger"); return render_template("application_form.html")
        app=CreditApplication(user_id=current_user.id,**data); result=predict(data)
        record=PredictionHistory(application=app,decision=result["decision"],probability=result["probability"],confidence=result["confidence"],risk_level=result["risk_level"],key_features="; ".join(result["key_features"]),model_name=result["model_name"])
        db.session.add_all([app,record]); db.session.commit(); return redirect(url_for("application.result",application_id=app.id))
    return render_template("application_form.html")
@application_bp.route("/result/<int:application_id>")
@login_required
def result(application_id):
    app=CreditApplication.query.filter_by(id=application_id,user_id=current_user.id).first_or_404(); return render_template("result.html",app=app,result=app.prediction)
@application_bp.route("/history")
@login_required
def history(): return render_template("history.html",apps=CreditApplication.query.filter_by(user_id=current_user.id).order_by(CreditApplication.submitted_at.desc()).all())
