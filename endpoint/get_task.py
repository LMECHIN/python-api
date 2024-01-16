from flask import request, jsonify
from flasgger import swag_from
from swagger.config import app
from token_api import authenticated_users
import connect_db

db = connect_db.db()


def requires_auth(func):
    def my_wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or "Bearer" not in auth_header:
            return jsonify({"error": "Unauthorized"}), 401

        token = auth_header.split(" ")[1]
        user = authenticated_users.get(token)

        if not user:
            return jsonify({"error": "Invalid token"}), 401

        return func(*args, **kwargs)

    return my_wrapper


# Utilisation de la syntaxe alternative pour ajouter des décorateurs
@app.route("/api/get_task", methods=["GET"])
@swag_from("../swagger/get_task.yml")
@requires_auth
def get_task():
    cursor = None

    try:
        cursor = db.cursor()
        query = "SELECT * FROM tasks;"
        cursor.execute(query)
        tasks = cursor.fetchall()

        # Convertir les résultats de la base de données en une liste de dictionnaires
        task_list = []
        for task in tasks:
            task_dict = {
                "task_id": task[0],
                "title": task[1],
                "description": task[2],
                "due_date": task[3],
                "status": task[4],
                "priority": task[5],
                "created_at": task[6],
                "updated_at": task[7],
            }
            task_list.append(task_dict)

        response = {"tasks": task_list}
        return jsonify(response)

    except Exception as e:
        print("Error:", str(e))
        response = {"error": str(e)}
        return jsonify(response), 500

    finally:
        if cursor is not None:
            cursor.close()
