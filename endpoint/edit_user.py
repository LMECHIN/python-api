from flask import request, jsonify
from flasgger import swag_from
from swagger.config import app
import connect_db

db = connect_db.db()

authenticated_users = {}


@app.route("/api/edit_user", methods=["POST"])
@swag_from("../swagger/edit_user.yml")
def edit_user():
    print(request.headers)
    try:
        token = request.headers.get("Authorization")

        if token is None or token not in authenticated_users:
            response = {"error": "Unauthorized - Invalid token"}
            return jsonify(response), 401

        user_data = authenticated_users[token]
        username = user_data["username"]
        email = user_data["email"]
        password = user_data["password"]

        if request.headers["Content-Type"] == "application/json":
            data = request.json
            new_username = data.get("new_username")
            new_email = data.get("new_email")
            new_password = data.get("new_password")
        else:
            data = request.form
            new_username = data.get("new_username")
            new_email = data.get("new_email")
            new_password = data.get("new_password")

        if not new_username or not new_email or not new_password:
            response = {"error": "No new data provided for update"}
            return jsonify(response), 400

        cursor = db.cursor()
        try:
            if new_username is not None:
                cursor.execute(
                    "UPDATE user SET username = %s WHERE username = %s;",
                    (new_username, username),
                )
                username = new_username

            if new_email is not None:
                cursor.execute(
                    "UPDATE user SET email = %s WHERE email = %s;", (new_email, email)
                )
                email = new_email

            if new_password is not None:
                cursor.execute(
                    "UPDATE user SET password = %s WHERE password = %s;",
                    (new_password, password),
                )
                password = new_password

            db.commit()
            response = {
                "message": "User data updated successfully",
                "username": username,
                "email": email,
                "password": password,
            }
            return jsonify(response), 200
        except Exception as e:
            db.rollback()
            response = {"error": f"Error updating user data: {str(e)}"}
            return jsonify(response), 500
        finally:
            cursor.close()

    except Exception as e:
        response = {"error": f"Error: {str(e)}"}
        return jsonify(response), 500
