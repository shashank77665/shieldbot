from backend.database import db
from datetime import timezone,datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=False, default="user.jpg")
    is_superuser = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"


class RequestLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    base_url = db.Column(db.String(255), nullable=False)
    options = db.Column(db.JSON, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    execution_time = db.Column(db.Float, nullable=True)
    result = db.Column(db.JSON, nullable=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class AppLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
