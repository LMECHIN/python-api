from flask import request, jsonify
from flasgger import swag_from
from src.swagger.config import app
from src.authenticate.auth import requires_auth, authenticated_users
import src.authenticate.connect_db as connect_db

routes = connect_db.routes()


@app.route(routes["endpoint_get_user"], methods=["GET"])
@swag_from(routes["swagger_get_user"])
@requires_auth
def get_user():
    token = request.headers.get("Authorization").split(" ")[1]
    user_data = authenticated_users.get(token)
    email = user_data.get("email")
    password = user_data.get("password")
    username = user_data.get("username")
    response = {"email": email, "password": password, "username": username}

    return jsonify(response)
