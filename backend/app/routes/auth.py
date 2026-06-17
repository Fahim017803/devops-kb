from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import AdminUser
from app import db

bp = Blueprint("auth", __name__, url_prefix="/api/admin")

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "username and password required"}), 400

    user = AdminUser.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user.username)
    return jsonify({"token": token, "username": user.username})

@bp.route("/me")
@jwt_required()
def me():
    return jsonify({"username": get_jwt_identity()})
