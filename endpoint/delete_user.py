from flask import request, jsonify
from flasgger import swag_from
from swagger.config import app
from token_api import authenticated_users
import connect_db

db = connect_db.db()


@app.route("/api/delete_user", methods=["DELETE"])
@swag_from("../swagger/delete_user.yml")
def delete_user():
    try:
        token = request.headers.get("Authorization")

        if token is None:
            response = {"error": "Token is missing"}
            return jsonify(response), 401

        if token in authenticated_users:
            user_data = authenticated_users[token]
            username = user_data.get("username")

            cursor = db.cursor()
            try:
                cursor.execute("DELETE FROM user WHERE username = %s;", (username,))
                db.commit()

                del authenticated_users[token]
                response = {"message": "User deleted successfully"}
                return jsonify(response)

            except Exception as e:
                db.rollback()
                response = {"error": f"Error deleting user: {str(e)}"}
                return jsonify(response), 500

            finally:
                cursor.close()

        else:
            response = {"error": "Invalid token"}
            return jsonify(response), 401

    except Exception as e:
        print("Error:", str(e))
        response = {"error": str(e)}
        return jsonify(response), 500
