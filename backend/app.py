#!/usr/bin/env python
from flask import Flask, redirect, request, session, jsonify, url_for
from datetime import timedelta, UTC
from backend.config import Config
from backend.database import db
import os
from dotenv import load_dotenv
from threading import Thread
from backend.monitor import monitor_running_tasks

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Set testing config if FLASK_ENV environment variable is 'testing'
    if os.getenv("FLASK_ENV") == "testing":
        app.config["TESTING"] = True
    else:
        app.config["TESTING"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SECURE"] = True  # Ensure HTTPS in production
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

    @app.before_request
    def enforce_authentication():
        # Public endpoints do not require an active session.
        public_paths = [
            "/auth/login", 
            "/auth/signup", 
            "/auth/reset-password", 
            "/auth/verify-token", 
            "/auth/refresh-token"
        ]
        # Allow static files and favicon.
        if request.path.startswith("/static") or request.path.startswith("/favicon"):
            return
        # If the path is public, allow it.
        if any(request.path.startswith(path) for path in public_paths):
            return
        # For all other paths, a valid session is required.
        if "user_id" not in session:
            # If JSON is expected, return JSON error.
            if request.is_json:
                return jsonify({"error": "Authentication required. Please log in or sign up."}), 401
            # Otherwise, redirect to the login page.
            return redirect(url_for("auth_v1.login"))

    return app

app = create_app()

if __name__ == '__main__':
    # Start the background monitor in a separate thread.
    monitor_thread = Thread(target=monitor_running_tasks, args=(app,), daemon=True)
    monitor_thread.start()
    
    app.run(host='0.0.0.0', port=5000, debug=True)