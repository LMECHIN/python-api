from flask import request, jsonify
from flasgger import swag_from
from swagger.config import app
from token_api import authenticated_users, requires_auth


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
