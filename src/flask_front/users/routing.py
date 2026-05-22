from flask import Flask, Blueprint, jsonify

users_bp = Blueprint(
        "users", 
    __name__, 
    url_prefix="/users",
    template_folder="templates"  # points to blueprints/users/templates
)

@users_bp.route("/", methods=["GET"])
def get_users():
    return jsonify({"message": "List of users"})

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify({"message": f"User {user_id}"})

@users_bp.route("/<int:user_id>/posts", methods=["GET"])
def get_user_posts(user_id):
    return jsonify({"message": f"Posts for user {user_id}"})