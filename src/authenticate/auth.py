from flask import request, jsonify, g

authenticated_users = {}


def requires_auth(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
        user = authenticated_users.get(token)

        if not user:
            return jsonify({"error": "Invalid token"}), 401

        g.user = user
        return func(*args, **kwargs)

    return wrapper
