from flask import request, jsonify
from flasgger import swag_from
from swagger.config import app
from token_api import generate_token, authenticated_users
import connect_db

db = connect_db.db()


@app.route("/api/login", methods=["POST"])
@swag_from("../swagger/login.yml")
def login():
    global token
    if request.headers["Content-Type"] == "application/json":
        data = request.json
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
    else:
        data = request.form
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")

    cursor = None

    try:
        cursor = db.cursor()

        update_query = "UPDATE user SET email = %s, password = %s, username = %s WHERE username = %s;"
        update_values = (email, password, username, username)
        cursor.execute(update_query, update_values)
        db.commit()

        select_query = "SELECT * FROM user WHERE email = %s AND password = %s;"
        select_values = (email, password)
        cursor.execute(select_query, select_values)
        user = cursor.fetchone()

        if user:
            if username is None:
                username = user[3]

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
                "username": username,
                "email": email,
                "password": password,
            }

            response = {"token": token, "message": "Login successful"}
            return jsonify(response)
        else:
            response = {"error": "Invalid email or password"}
            return jsonify(response), 401

    except Exception as e:
        print("Error:", str(e))
        response = {"error": str(e)}
        return jsonify(response), 500

    finally:
        if cursor is not None:
            cursor.close()
