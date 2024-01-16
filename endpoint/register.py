from flask import request, jsonify
from flasgger import swag_from
from swagger.config import app
from token_api import generate_token, authenticated_users
import connect_db

db = connect_db.db()


@app.route("/api/register", methods=["POST"])
@swag_from("../swagger/register.yml")
def register():
    if request.headers["Content-Type"] == "application/json":
        data = request.json
        name = data.get("username")
        email = data.get("email")
        password = data.get("password")
    else:
        data = request.form
        name = data.get("username")
        email = data.get("email")
        password = data.get("password")

    if not name or not email or not password:
        error_message = "Please provide values for username, email, and password."
        response = {"error": error_message}
        return jsonify(response), 400

    cursor = None

    try:
        cursor = db.cursor()
        query = "INSERT INTO user (email, password, username) VALUES (%s, %s, %s);"
        values = (email, password, name)
        cursor.execute(query, values)
        db.commit()
        existing_token = next(
            (
                token
                for token, user_data in authenticated_users.items()
                if user_data["email"] == email
            ),
            None,
        )

        if existing_token:
            del authenticated_users[existing_token]

        token = generate_token()
        print(token)
        authenticated_users[token] = {
            "username": name,
            "email": email,
            "password": password,
        }

        response = {"token": token, "message": "User registered successfully"}

        return jsonify(response)

    except Exception as e:
        print("Error:", str(e))
        response = {"error": str(e)}

        return jsonify(response), 500

    finally:
        if cursor is not None:
            cursor.close()
