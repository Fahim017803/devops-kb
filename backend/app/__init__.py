import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db  = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from app.routes import articles, auth, admin
    app.register_blueprint(articles.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)

    # ── Ensure tables exist + seed default admin ──────────
    # This runs on every app startup (works with gunicorn AND `python run.py`)
    with app.app_context():
        db.create_all()
        from app.models import AdminUser
        if not AdminUser.query.first():
            admin_user = AdminUser(username="admin")
            admin_user.set_password(os.environ.get("ADMIN_PASSWORD", "devops123"))
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Default admin created: admin / " + os.environ.get("ADMIN_PASSWORD", "devops123"))

    return app
