import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta
from backend.models import ShieldbotUser  # Updated to reflect the new model name
from backend.database import db
from dotenv import load_dotenv
from backend.config import Config
import os
# Load environment variables
load_dotenv()

# Secret key and token expiration settings
SECRET_KEY = os.getenv("SECRET_KEY", "you-will-never-guess")
TOKEN_EXPIRY_HOURS = int(os.getenv("TOKEN_EXPIRY_HOURS", 1))

def create_jwt(user_id: int, expires_in: int = 3600):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "Token expired"
    except Exception as e:
        return None, str(e)

def decode_and_verify_token(token):
    """
    Decode and verify a JWT token.
    Returns the ShieldbotUser object if valid, else returns an error message.
    """
    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = ShieldbotUser.query.get(payload.get("shieldbot_user_id"))
        if user:
            return user, None
        return None, "User not found"
    except jwt.ExpiredSignatureError:
        return None, "Token expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"
