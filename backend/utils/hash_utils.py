import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(hashed: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
