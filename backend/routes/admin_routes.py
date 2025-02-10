from flask import Blueprint, request, jsonify
from backend.models import ShieldbotUser, Test  # Use ShieldbotUser instead of User
from backend.utils.jwt_utils import decode_jwt

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def get_user_from_token(req):
    token = req.headers.get("Authorization", "")
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    payload, _ = decode_jwt(token)
    if payload:
        return ShieldbotUser.query.get(payload.get("user_id"))
    return None

def is_admin(user):
    return user and user.is_superuser

@admin_bp.route("/users", methods=["GET"])
def view_all_users():
    user = get_user_from_token(request)
    if not user or not is_admin(user):
        return jsonify({"error": "Unauthorized"}), 401
    all_users = ShieldbotUser.query.all()
    users_data = []
    for u in all_users:
        users_data.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "email_verified": u.email_verified,
            "is_superuser": u.is_superuser,
            "tests": [{"id": t.id, "test_name": t.test_name, "status": t.status} for t in getattr(u, "tests", [])]
        })
    return jsonify({"users": users_data}), 200

@admin_bp.route("/tests", methods=["GET"])
def view_all_tests():
    user = get_user_from_token(request)
    if not user or not is_admin(user):
        return jsonify({"error": "Unauthorized"}), 401
    tests = Test.query.all()
    tests_list = []
    for t in tests:
        tests_list.append({
            "id": t.id,
            "user_id": t.user_id,
            "test_name": t.test_name,
            "base_url": t.base_url,
            "status": t.status,
            "start_time": t.start_time.isoformat() if t.start_time else None,
            "end_time": t.end_time.isoformat() if t.end_time else None,
            "logs": t.logs,
            "ai_insights": t.ai_insights
        })
    return jsonify({"tests": tests_list}), 200 