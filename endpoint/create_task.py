from flask import request, jsonify
from flasgger import swag_from
from swagger.config import app
import connect_db

db = connect_db.db()


@app.route("/api/create_task", methods=["POST"])
@swag_from("../swagger/create_task.yml")
def create_task():
    if request.headers["Content-Type"] == "application/json":
        data = request.json
        title = data.get("title")
        description = data.get("description")
        due_date = data.get("due_date")
        status = data.get("status", "To Do")  # Default to "To Do" if not provided
        priority = data.get("priority", "Medium")  # Default to "Medium" if not provided
    else:
        data = request.form
        title = data.get("title")
        description = data.get("description")
        due_date = data.get("due_date")
        status = data.get("status", "To Do")  # Default to "To Do" if not provided
        priority = data.get("priority", "Medium")  # Default to "Medium" if not provided

    if not title:
        error_message = "Please provide a title for the task."
        response = {"error": error_message}
        return jsonify(response), 400

    cursor = None

    try:
        cursor = db.cursor()
        query = """
            INSERT INTO tasks (title, description, due_date, status, priority)
            VALUES (%s, %s, %s, %s, %s);
        """
        values = (title, description, due_date, status, priority)
        cursor.execute(query, values)
        db.commit()

        task_id = cursor.lastrowid  # Get the ID of the newly inserted task
        response = {"message": "Task created successfully", "task_id": task_id}

        return jsonify(response)

    except Exception as e:
        print("Error:", str(e))
        response = {"error": str(e)}
        return jsonify(response), 500

    finally:
        if cursor is not None:
            cursor.close()
