from flask import request, jsonify
from flasgger import swag_from
from swagger.config import app
import connect_db

db = connect_db.db()


@app.route("/api/register", methods=["POST"])
@swag_from("../swagger/register.yml")
def register():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        name = data.get("username")
        email = data.get("email")
        password = data.get("password")
    else:
        data = request.form
        name = data.get("username")
        email = data.get("email")
        password = data.get("password")

    cursor = None

    try:
        cursor = db.cursor()
        query = "INSERT INTO user (email, password, username) VALUES (%s, %s, %s);"
        values = (email, password, name)
        cursor.execute(query, values)
        db.commit()
        response = {"message": "User registered successfully"}

        return jsonify(response)

    except Exception as e:
        print("Error:", str(e))
        response = {"error": str(e)}

        return jsonify(response), 500

    finally:
        if cursor is not None:
            cursor.close()
