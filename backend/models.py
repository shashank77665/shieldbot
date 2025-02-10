from backend.database import db
from datetime import timezone, datetime

class ShieldbotUser(db.Model):
    __tablename__ = "shieldbot_users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to tests (each user can have many tests)
    tests = db.relationship('Test', backref='user', lazy=True)

    def __repr__(self):
        return f"<ShieldbotUser {self.username}>"

    @staticmethod
    def validate_fields(data):
        """Validate and truncate fields to conform to database constraints."""
        data["username"] = data.get("username", "")[:80]
        data["email"] = data.get("email", "")[:120]
        return data

# Create an alias so that 'User' can be imported in other modules.
User = ShieldbotUser

class Test(db.Model):
    __tablename__ = "tests"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("shieldbot_users.id"), nullable=False)
    test_name = db.Column(db.String(100), nullable=False)
    base_url = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    logs = db.Column(db.JSON, nullable=True)
    ai_insights = db.Column(db.JSON, nullable=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)

class RequestLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shieldbot_user_id = db.Column(
        db.Integer, db.ForeignKey("shieldbot_users.id"), nullable=False
    )
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
