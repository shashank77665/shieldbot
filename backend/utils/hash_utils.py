import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    try:
        # Ensure the hashed string is a valid bcrypt hash before checking.
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except ValueError:
        # The stored hash does not have a valid salt (possibly legacy data or malformed value).
        return False
