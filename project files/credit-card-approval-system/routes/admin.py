from flask import Blueprint, abort, render_template, request
from flask_login import login_required, current_user
from services.database import User, CreditApplication, PredictionHistory
from ml.predictor import model_metrics
admin_bp=Blueprint("admin",__name__,url_prefix="/admin")
def guard():
    if current_user.email!="admin@example.com": abort(403)
@admin_bp.route("/")
@login_required
def dashboard():
    guard(); q=request.args.get("q","").strip(); users=User.query
    if q: users=users.filter(User.email.contains(q) | User.full_name.contains(q))
    applications=CreditApplication.query.order_by(CreditApplication.submitted_at.desc()).limit(100).all()
    return render_template("admin.html",users=users.order_by(User.created_at.desc()).all(),applications=applications,apps=applications,predictions=PredictionHistory.query.order_by(PredictionHistory.created_at.desc()).limit(100).all(),metrics=model_metrics())
