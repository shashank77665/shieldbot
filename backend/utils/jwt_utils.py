import os
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta
from backend.models import User
from backend.database import db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
TOKEN_EXPIRY_HOURS = int(os.getenv("TOKEN_EXPIRY_HOURS", 1))

def create_jwt(user_id):
    """
    Create a JWT token for a user.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token  # Already a string, no need to decode



def decode_and_verify_token(token):
    """
    Decode and verify a JWT token.
    Returns the user object if valid, else returns an error message.
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = db.session.get(User, decoded["user_id"])  # Modern SQLAlchemy method
        if not user:
            return None, "Invalid user"
        return user, None
    except ExpiredSignatureError:
        return None, "Token has expired"
    except InvalidTokenError:
        return None, "Invalid token"
