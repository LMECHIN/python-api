from flask import request, jsonify, g
from flasgger import swag_from
from src.swagger.config import app
from src.authenticate.auth import requires_auth
import src.authenticate.connect_db as connect_db

db = connect_db.db()
routes = connect_db.routes()


@swag_from(routes["swagger_create_task"])
@requires_auth
def create_task():
    user_id = g.user.get("id")

    if request.headers["Content-Type"] == "application/json":
        data = request.json
        title = data.get("title")
        description = data.get("description")
        due_date = data.get("due_date")
        status = data.get("status", "To Do")
        priority = data.get("priority", "Medium")
    else:
        data = request.form
        title = data.get("title")
        description = data.get("description")
        due_date = data.get("due_date")
        status = data.get("status", "To Do")
        priority = data.get("priority", "Medium")

    if not title:
        error_message = "Please provide a title for the task."
        response = {"error": error_message}
        return jsonify(response), 400

    cursor = None

    try:
        cursor = db.cursor()
        query = """
            INSERT INTO tasks (user_id, title, description, due_date, status, priority)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        values = (user_id, title, description, due_date, status, priority)
        cursor.execute(query, values)
        db.commit()

        task_id = cursor.lastrowid
        response = {"message": "Task created successfully", "task_id": task_id}

        return jsonify(response)

    except Exception as e:
        print("Error:", str(e))
        response = {"error": str(e)}
        return jsonify(response), 500

    finally:
        if cursor is not None:
            cursor.close()


app.add_url_rule(routes["endpoint_create_task"], "create_task", create_task, methods=["POST"])
