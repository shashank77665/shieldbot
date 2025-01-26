import os
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta
from backend.models import ShieldbotUser  # Updated to reflect the new model name
from backend.database import db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Secret key and token expiration settings
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
TOKEN_EXPIRY_HOURS = int(os.getenv("TOKEN_EXPIRY_HOURS", 1))

def create_jwt(shieldbot_user_id):
    """
    Create a JWT token for a Shieldbot user.
    """
    payload = {
        "shieldbot_user_id": shieldbot_user_id,  # Updated to match the new naming convention
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_and_verify_token(token):
    """
    Decode and verify a JWT token.
    Returns the ShieldbotUser object if valid, else returns an error message.
    """
    try:
        # Decode the token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Fetch the user from the database using the shieldbot_user_id in the payload
        shieldbot_user = db.session.get(ShieldbotUser, decoded["shieldbot_user_id"])  # Modern SQLAlchemy method
        if not shieldbot_user:
            return None, "Invalid user"
        return shieldbot_user, None
    except ExpiredSignatureError:
        return None, "Token has expired"
    except InvalidTokenError:
        return None, "Invalid token"
