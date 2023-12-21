from flask import request, jsonify
import secrets

authenticated_users = {}

def requires_auth(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer' not in auth_header:
            return jsonify({"error": "Unauthorized"}), 401

        token = auth_header.split(' ')[1]
        user = authenticated_users.get(token)

        if not user:
            return jsonify({"error": "Invalid token"}), 401

        return func(*args, **kwargs)

    return wrapper


def generate_token():
    return secrets.token_hex(16)
