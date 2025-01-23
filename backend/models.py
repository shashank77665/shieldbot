from backend.database import db
from datetime import timezone, datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=False, default="user.jpg")
    is_superuser = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"

    @staticmethod
    def validate_fields(data):
        """Validate and truncate fields to conform to database constraints."""
        data["username"] = data.get("username", "")[:50]
        data["email"] = data.get("email", "")[:120]
        data["profile_picture"] = data.get("profile_picture", "user.jpg")[:255]
        return data


class RequestLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    base_url = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    execution_time = db.Column(db.Float, nullable=True)
    result = db.Column(db.JSON, nullable=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @staticmethod
    def validate_fields(data):
        """Validate and truncate fields to conform to database constraints."""
        data["test_type"] = data.get("test_type", "")[:50]
        data["base_url"] = data.get("base_url", "")[:255]
        data["status"] = data.get("status", "Pending")[:50]
        return data

class AppLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))