from backend.models import db, User
from backend.utils.hash_utils import hash_password
from sqlalchemy.exc import IntegrityError


def create_user(username, email, password, is_superuser=False):
    """
    Create a user or superuser in the database.

    Args:
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The plaintext password of the user.
        is_superuser (bool): Whether the user is a superuser.

    Returns:
        dict: A success message or error message.
    """
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return {"error": f"User with username '{username}' or email '{email}' already exists."}

    hashed_password = hash_password(password)
    user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        is_superuser=is_superuser,
    )

    try:
        db.session.add(user)
        db.session.commit()
        return {"success": f"User '{username}' created successfully."}
    except IntegrityError as e:
        db.session.rollback()
        return {"error": f"Database error: {str(e)}"}


def delete_user_by_email(email):
    """
    Delete a user from the database by email.

    Args:
        email (str): The email of the user.

    Returns:
        dict: A success or error message.
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": f"No user found with email '{email}'."}

    db.session.delete(user)
    db.session.commit()
    return {"success": f"User with email '{email}' deleted successfully."}
