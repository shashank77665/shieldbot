import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta, UTC
from backend.models import ShieldbotUser  # Updated to reflect the new model name
from backend.database import db
from dotenv import load_dotenv
from backend.config import Config
import os
from flask import current_app
# Load environment variables
load_dotenv()

# Secret key and token expiration settings
SECRET_KEY = os.getenv("SECRET_KEY", "you-will-never-guess")
TOKEN_EXPIRY_HOURS = int(os.getenv("TOKEN_EXPIRY_HOURS", 1))

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "Token expired"
    except Exception as e:
        return None, str(e)
def create_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(UTC)+ timedelta(minutes=30)
    }
    token = jwt.encode(payload, current_app.secret_key, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    current_app.logger.debug("Created JWT payload: %s", payload)
    return token

def decode_and_verify_token(token):
    try:
        payload = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
        current_app.logger.debug("Decoded JWT payload: %s", payload)
        user = ShieldbotUser.query.get(payload.get("user_id"))
        if not user:
            return None, "User does not exist."
        return user, None
    except jwt.ExpiredSignatureError:
        return None, "Token has expired."
    except jwt.InvalidTokenError as e:
        return None, "Invalid token: " + str(e)
