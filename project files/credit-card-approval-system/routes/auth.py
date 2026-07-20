from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from services.database import db, User
auth_bp=Blueprint("auth",__name__,url_prefix="/auth")
@auth_bp.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:return redirect(url_for("application.dashboard"))
    if request.method=="POST":
        name=request.form.get("full_name","").strip(); email=request.form.get("email","").lower().strip(); password=request.form.get("password","")
        if len(name)<2 or "@" not in email or len(password)<8: flash("Enter a name, a valid email, and a password of at least 8 characters.","danger")
        elif User.query.filter_by(email=email).first(): flash("That email is already registered.","warning")
        else:
            user=User(full_name=name,email=email); user.set_password(password); db.session.add(user); db.session.commit(); login_user(user); return redirect(url_for("application.dashboard"))
    return render_template("register.html")
@auth_bp.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:return redirect(url_for("application.dashboard"))
    if request.method=="POST":
        user=User.query.filter_by(email=request.form.get("email","").lower().strip()).first()
        if user and user.check_password(request.form.get("password", "")):
            login_user(user,remember=bool(request.form.get("remember"))); return redirect(request.args.get("next") or url_for("application.dashboard"))
        flash("Incorrect email or password.","danger")
    return render_template("login.html")
@auth_bp.route("/logout")
@login_required
def logout(): logout_user(); flash("You have been signed out.","success"); return redirect(url_for("main.home"))
@auth_bp.route("/forgot-password",methods=["GET","POST"])
def forgot_password():
    if request.method=="POST": flash("If the email exists, password-reset instructions have been queued. Configure an email provider in production.","info"); return redirect(url_for("auth.login"))
    return render_template("forgot_password.html")
