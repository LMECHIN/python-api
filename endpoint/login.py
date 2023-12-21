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
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        email = data.get("email")
        password = data.get("password")
    else:
        data = request.form
        email = data.get("email")
        password = data.get("password")

    cursor = None

    try:
        cursor = db.cursor()
        query = "SELECT * FROM user WHERE email = %s AND password = %s;"
        values = (email, password)
        cursor.execute(query, values)
        user = cursor.fetchone()

        if user:
            response = {"message": "Login successful"}
            token = generate_token()
            print(token)
            authenticated_users[token] = {"email": email, "password": password}
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
