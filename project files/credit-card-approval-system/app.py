from flask import Flask
from flask_login import LoginManager
from config import Config
from services.database import db

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["SQLALCHEMY_DATABASE_URI"] = str(app.config["SQLALCHEMY_DATABASE_URI"])
    db.init_app(app)
    login_manager.init_app(app)

    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.application import application_bp
    from routes.admin import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(admin_bp)

    @login_manager.user_loader
    def load_user(user_id):
        from services.database import User
        return db.session.get(User, int(user_id))

    with app.app_context():
        from services.database import seed_admin
        db.create_all()
        seed_admin()

    return app


if __name__ == "__main__":
    create_app().run(debug=True, host="0.0.0.0", port=5000)
