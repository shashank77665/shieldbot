import unittest
from backend.app import app, db
from backend.models import User, RequestLog
from backend.utils.hash_utils import hash_password
from datetime import datetime, timedelta, timezone
import jwt
import os
def generate_valid_token(user_id=1):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(payload, os.getenv("SECRET_KEY", "your_secret_key"), algorithm="HS256")

class AttackRoutesTestCase(unittest.TestCase):
    def setUp(self):
        """Setup the test environment and database."""
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
            db.create_all()

            # Create a default user
            user = User(
                username="testuser",
                email="test@example.com",
                password_hash=hash_password("password123"),
            )
            db.session.add(user)
            db.session.commit()

            self.user = user
            self.valid_token = jwt.encode(
                {"user_id": user.id, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
                os.getenv("SECRET_KEY", "your_secret_key"),
                algorithm="HS256",
            )
            self.expired_token = jwt.encode(
                {"user_id": user.id, "exp": datetime.now(timezone.utc) - timedelta(hours=1)},
                os.getenv("SECRET_KEY", "your_secret_key"),
                algorithm="HS256",
            )
    def test_perform_test_missing_username_for_brute_force(self):
        token = generate_valid_token()
        response = self.app.post(
            "/attack/perform-test",
            headers={"Authorization": token},
            json={
                "base_url": "http://example.com",
                "attack_selection": {"brute_force": True}
                # intentionally missing "username"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username is required for brute force attack", response.get_data(as_text=True))

    def tearDown(self):
        """Teardown the test environment."""
        with app.app_context():
            db.session.close()
            db.session.remove()
            db.drop_all()

    def test_perform_test_valid(self):
        """Test a valid attack submission."""
        response = self.app.post(
            "/attack/perform-test",
            headers={"Authorization": self.valid_token},
            json={
                "base_url": "http://example.com",
                "attack_selection": {"sql_injection": True},
            },
        )
        self.assertEqual(response.status_code, 202)
        self.assertIn("task_id", response.get_json())

    def test_perform_test_missing_token(self):
        response = self.app.post(
            "/attack/perform-test",
            json={"base_url": "http://example.com", "attack_selection": {"sql_injection": True}},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Token is missing", response.get_data(as_text=True))

    def test_perform_test_expired_token(self):
        response = self.app.post(
            "/attack/perform-test",
            headers={"Authorization": self.expired_token},
            json={"base_url": "http://example.com", "attack_selection": {"sql_injection": True}},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Token has expired", response.get_data(as_text=True))

    def test_task_status_valid(self):
        """Test checking task status with a valid task ID."""
        task_id = "valid_task_id_example"  # Replace with an actual task ID for real integration tests
        response = self.app.get(
            f"/attack/task-status/{task_id}",
            headers={"Authorization": self.valid_token},
        )
        self.assertIn(response.status_code, [200, 202])  # Depending on task state

    def test_task_status_missing_token(self):
        task_id = "valid_task_id_example"
        response = self.app.get(f"/attack/task-status/{task_id}")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Token is missing", response.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
