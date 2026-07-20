from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    applications = db.relationship("CreditApplication", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)


class Admin(UserMixin, db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class CreditApplication(db.Model):
    __tablename__ = "credit_applications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    age = db.Column(db.Integer, nullable=False); gender = db.Column(db.String(30), nullable=False)
    annual_income = db.Column(db.Float, nullable=False); employment_type = db.Column(db.String(40), nullable=False)
    employment_duration = db.Column(db.Float, nullable=False); education = db.Column(db.String(40), nullable=False)
    marital_status = db.Column(db.String(40), nullable=False); existing_loan_amount = db.Column(db.Float, nullable=False)
    credit_inquiries = db.Column(db.Integer, nullable=False); credit_history = db.Column(db.Float, nullable=False)
    monthly_income = db.Column(db.Float, nullable=False); outstanding_debt = db.Column(db.Float, nullable=False)
    payment_history = db.Column(db.Float, nullable=False); housing_type = db.Column(db.String(40), nullable=False)
    occupation = db.Column(db.String(60), nullable=False)
    user = db.relationship("User", back_populates="applications")
    prediction = db.relationship("PredictionHistory", back_populates="application", uselist=False, cascade="all, delete-orphan")


class PredictionHistory(db.Model):
    __tablename__ = "prediction_history"
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("credit_applications.id"), unique=True, nullable=False)
    decision = db.Column(db.String(20), nullable=False)
    probability = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    key_features = db.Column(db.Text, nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    application = db.relationship("CreditApplication", back_populates="prediction")


def seed_admin():
    if not Admin.query.filter_by(email="admin@example.com").first():
        admin = Admin(name="System Administrator", email="admin@example.com")
        admin.password_hash = generate_password_hash("Admin123!")
        db.session.add(admin); db.session.commit()
