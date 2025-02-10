#!/usr/bin/env python
from flask import Flask
from backend.config import Config
from backend.database import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Set testing config if FLASK_ENV environment variable is 'testing'
    if os.getenv("FLASK_ENV") == "testing":
        app.config["TESTING"] = True
    else:
        app.config["TESTING"] = False

    db.init_app(app)

    # Only initialize Flask-Migrate if not in testing mode to avoid SQLAlchemy typing errors
    if not app.config.get("TESTING"):
        from flask_migrate import Migrate
        Migrate(app, db)

    # Import and register blueprints
    from backend.routes.auth_routes import auth_bp
    from backend.routes.attack_routes import attack_bp
    from backend.routes.dashboard_routes import dashboard_bp
    from backend.routes.custom_test_routes import custom_tests_bp
    from backend.routes.test_routes import test_bp
    from backend.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(attack_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(custom_tests_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(admin_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)