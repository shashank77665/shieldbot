from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    hashed = generate_password_hash(password)
    # Truncate hashed password to the database limit
    return hashed[:256]

def verify_password(hash, password):
    return check_password_hash(hash, password)
