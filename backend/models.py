from backend.database import db
from datetime import timezone, datetime, timedelta
import time
from celery.result import AsyncResult

class ShieldbotUser(db.Model):
    __tablename__ = "shieldbot_users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(256), default="user.jpg")
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

    @property
    def shieldbot_user_id(self):
        """Alias for the primary key, used in JWT creation and elsewhere."""
        return self.id

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
    celery_task_id = db.Column(db.String(128), nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    celery_task_id = db.Column(db.String(128), nullable=True)
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                             onupdate=lambda: datetime.now(timezone.utc))

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

def monitor_tests(app, check_interval=10, timeout_threshold=20):
    """
    Additional monitor logic for the Test model – similar to the RequestLog
    monitor but if you need to cover both models separately.
    """
    with app.app_context():
        while True:
            now = datetime.now(timezone.utc)
            tests_to_check = Test.query.filter(Test.status.in_(["Pending", "Running"])).all()
            tests_updated = False
            for test in tests_to_check:
                # Use last_updated if available; fall back on start_time.
                last_update = test.last_updated or test.start_time
                if last_update.tzinfo is None:
                    last_update = last_update.replace(tzinfo=timezone.utc)
                if now - last_update > timedelta(seconds=timeout_threshold):
                    test.status = "Aborted"
                    tests_updated = True

                # Check celery state if a celery_task_id is available.
                if test.celery_task_id:
                    celery_result = AsyncResult(test.celery_task_id)
                    if celery_result.state != test.status:
                        test.status = celery_result.state
                        # Optionally update logs and end_time if finished.
                        if celery_result.state in ['SUCCESS', 'FAILURE']:
                            test.end_time = datetime.now(timezone.utc)
                        tests_updated = True
            if tests_updated:
                db.session.commit()
            time.sleep(check_interval)
