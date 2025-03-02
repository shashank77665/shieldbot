#!/usr/bin/env python
from flask import Flask, jsonify, url_for, session
from datetime import timedelta, UTC
from backend.config import Config
from backend.database import db
import os
from dotenv import load_dotenv
from threading import Thread
from backend.monitor import monitor_running_tasks
from flask_cors import CORS
import uuid
from celery import Celery

def create_celery(app):
    """Create and configure Celery instance"""
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Session configuration remains for legacy or other purposes,
    # but is not used for enforcing authentication exclusively.
    app.config['SESSION_COOKIE_NAME'] = 'my_app_session'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False 

    # Enable CORS for development
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Set testing config if FLASK_ENV environment variable is 'testing'
    app.config["TESTING"] = os.getenv("FLASK_ENV") == "testing"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SECURE"] = True  # Ensure HTTPS in production

    db.init_app(app)

    # Initialize Flask-Migrate when not testing.
    if not app.config.get("TESTING"):
        from flask_migrate import Migrate
        Migrate(app, db)

    # Import and register blueprints.
    from backend.routes.auth_routes import auth_bp
    from backend.routes.attack_routes import attack_bp
    from backend.routes.dashboard_routes import dashboard_bp
    from backend.routes.custom_test_routes import custom_tests_bp
    from backend.routes.test_routes import test_bp
    from backend.routes.admin_routes import admin_bp
    from backend.routes.main_routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(attack_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(custom_tests_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)

    # No global session-based authentication is enforced.
    
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    # Initialize Celery
    celery = create_celery(app)
    app.extensions["celery"] = celery

    return app

app = create_app()

if __name__ == '__main__':
    # Start the background monitor in a separate thread.
    monitor_thread = Thread(target=monitor_running_tasks, args=(app,), daemon=True)
    monitor_thread.start()
    
    app.run(host='0.0.0.0', port=5000, debug=True)