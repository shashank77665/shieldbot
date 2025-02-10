from backend.models import db, ShieldbotUser, RequestLog
from backend.utils.hash_utils import hash_password
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from backend.utils.auth_decorator import authorize


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
    if ShieldbotUser.query.filter((ShieldbotUser.username == username) | (ShieldbotUser.email == email)).first():
        return {"error": f"User with username '{username}' or email '{email}' already exists."}

    hashed_password = hash_password(password)
    user = ShieldbotUser(
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
    user = ShieldbotUser.query.filter_by(email=email).first()
    if not user:
        return {"error": f"No user found with email '{email}'."}

    db.session.delete(user)
    db.session.commit()
    return {"success": f"User with email '{email}' deleted successfully."}


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/user-activities", methods=["GET"])
@authorize(required_superuser=True)
def user_activities():
    """
    Superuser view of user test activities.
    Returns a list of users along with their recent (up to 5) test logs.
    """
    users = ShieldbotUser.query.all()
    activities = []
    for user in users:
        tests = RequestLog.query.filter_by(
            shieldbot_user_id=user.shieldbot_user_id
        ).order_by(RequestLog.timestamp.desc()).limit(5).all()
        test_list = []
        for test in tests:
            test_list.append({
                "test_id": test.id,
                "base_url": test.base_url,
                "status": test.status,
                "timestamp": test.timestamp.isoformat(),
                "test_type": test.test_type
            })
        activities.append({
            "user_id": user.shieldbot_user_id,
            "username": user.username,
            "email": user.email,
            "recent_tests": test_list
        })
    return jsonify({"activities": activities}), 200
