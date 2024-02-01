from flask import request, jsonify
from flasgger import swag_from
from src.swagger.config import app
from src.authenticate.auth import authenticated_users
import src.authenticate.connect_db as connect_db

db = connect_db.db()
routes = connect_db.routes()


@app.route(routes["endpoint_logout"], methods=["POST"])
@swag_from(routes["swagger_logout"])
def logout():
    try:
        token = request.headers.get("Authorization")

        if token is None:
            response = {"error": "Token is missing"}
            return jsonify(response), 401

        if token in authenticated_users:
            del authenticated_users[token]
            response = {"message": "Logout successful"}
            return jsonify(response)
        else:
            response = {"error": "Invalid token"}
            return jsonify(response), 401

    except Exception as e:
        print("Error:", str(e))
        response = {"error": str(e)}
        return jsonify(response), 500
