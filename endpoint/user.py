from flask import request, jsonify
from flasgger import swag_from
from swagger.config import app
from token_api import authenticated_users


def requires_auth(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or "Bearer" not in auth_header:
            return jsonify({"error": "Unauthorized"}), 401

        token = auth_header.split(" ")[1]
        user = authenticated_users.get(token)

        if not user:
            return jsonify({"error": "Invalid token"}), 401

        return func(*args, **kwargs)

    return wrapper


@app.route("/api/user", methods=["GET"])
@swag_from("../swagger/user.yml")
@requires_auth
def user():
    token = request.headers.get("Authorization").split(" ")[1]
    user_data = authenticated_users.get(token)
    email = user_data.get("email")
    password = user_data.get("password")
    username = user_data.get("username")
    response = {"email": email, "password": password, "username": username}

    return jsonify(response)
