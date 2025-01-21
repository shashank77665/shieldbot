import os
from flask import Flask
from flask_cors import CORS
from logging_config import setup_logging
from database import db, migrate
from app_routes.auth_routes import auth_bp
from app_routes.attack_routes import attack_bp

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Configure Flask App
app.config.from_object("config.Config")

# Set up logger
logger = setup_logging("ShieldBotAPI")

# Initialize Extensions
db.init_app(app)
migrate.init_app(app, db)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(attack_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
