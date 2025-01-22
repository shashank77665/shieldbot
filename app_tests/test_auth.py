import unittest
from app import app, db
from models import User
from utils.hash_utils import hash_password
import jwt
from datetime import datetime, timedelta, timezone
import os
import json

class AuthRoutesTestCase(unittest.TestCase):
    def setUp(self):
        """Setup the test environment and database."""
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
            db.create_all()

            # Create a default user with a hashed password
            user = User(
                username="testuser",
                email="test@example.com",
                password_hash=hash_password("password123"),
            )
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        """Teardown the test environment."""
        with app.app_context():
            db.session.close()
            db.session.remove()
            db.drop_all()

    def test_signup_success(self):
        response = self.app.post(
            "/auth/signup",
            json={"username": "newuser", "email": "new@example.com", "password": "password123"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("User registered successfully", response.get_data(as_text=True))

    def test_signup_duplicate(self):
        response = self.app.post(
            "/auth/signup",
            json={"username": "testuser", "email": "test@example.com", "password": "password123"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("User already exists", response.get_data(as_text=True))

    def test_login_success(self):
        response = self.app.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.get_json())

    def test_login_failure(self):
        response = self.app.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid email or password", response.get_data(as_text=True))

    def test_verify_token_success(self):
        login_response = self.app.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = login_response.get_json().get("token")

        response = self.app.get(
            "/auth/verify-token",
            headers={"Authorization": token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Token is valid", response.get_data(as_text=True))
        self.assertIn("user_id", response.get_json())

    def test_verify_token_expired(self):
        # Generate an expired token
        expired_token = jwt.encode(
            {"user_id": 1, "exp": datetime.now(timezone.utc) - timedelta(hours=1)},
            os.getenv("SECRET_KEY", "default_secret_key"),
            algorithm="HS256",
        )
        response = self.app.get(
            "/auth/verify-token",
            headers={"Authorization": expired_token},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Token has expired", response.get_data(as_text=True))

    def test_verify_token_missing(self):
        response = self.app.get("/auth/verify-token")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Token is missing", response.get_data(as_text=True))

    def test_refresh_token_success(self):
        login_response = self.app.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = login_response.get_json().get("token")

        response = self.app.post(
            "/auth/refresh-token",
            headers={"Authorization": token},
        )
        self.assertIn(response.status_code, [200, 400])  # 400 if token is still valid
        
    def test_signup_missing_email(self):
        response = self.app.post(
            "/auth/signup",
            json={"username": "newuser", "password": "password123"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing fields", response.get_data(as_text=True))
        

if __name__ == "__main__":
    unittest.main()
