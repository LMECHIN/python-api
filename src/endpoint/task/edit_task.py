from flask import request, jsonify, g
from flasgger import swag_from
from src.swagger.config import app
from src.authenticate.auth import requires_auth
import src.authenticate.connect_db as connect_db

db = connect_db.db()
routes = connect_db.routes()


@swag_from(routes["swagger_edit_task"])
@requires_auth
def edit_task():
    user_id = g.user.get("id")

    if request.headers["Content-Type"] == "application/json":
        data = request.json
        task_id = data.get("task_id")
        new_title = data.get("new_title")
        new_description = data.get("new_description")
        new_status = data.get("new_status")
        new_priority = data.get("new_priority")
    else:
        data = request.form
        task_id = data.get("task_id")
        new_title = data.get("new_title")
        new_description = data.get("new_description")
        new_status = data.get("new_status")
        new_priority = data.get("new_priority")

    cursor = None

    try:
        cursor = db.cursor()

        cursor.execute("SELECT * FROM tasks WHERE user_id = %s AND task_id = %s;", (user_id, task_id))
        task_data = cursor.fetchone()
        if not task_data:
            response = {"error": "Task not found"}
            return jsonify(response), 404

        title, description, status, priority = (
            task_data[2],
            task_data[3],
            task_data[5],
            task_data[6],
        )
        # cursor.fetchall()
        print(task_id)
        print(title)
        print(description)
        print(status)
        print(priority)
        print(task_id)

        if new_title is not None:
            query = "UPDATE tasks SET title = %s WHERE title = %s AND user_id = %s AND task_id = %s;"
            cursor.execute(query, (new_title, title, user_id, task_id))
            title = new_title

        if new_description is not None:
            cursor.execute(
                "UPDATE tasks SET description = %s WHERE description = %s AND user_id = %s AND task_id = %s;",
                (new_description, description, user_id, task_id),
            )
            description = new_description

        if new_status is not None:
            cursor.execute(
                "UPDATE tasks SET status = %s WHERE status = %s AND user_id = %s AND task_id = %s;",
                (new_status, status, user_id, task_id),
            )
            status = new_status

        if new_priority is not None:
            cursor.execute(
                "UPDATE tasks SET priority = %s WHERE priority = %s AND user_id = %s AND task_id = %s;",
                (new_priority, priority, user_id, task_id),
            )
            priority = new_priority

        db.commit()
        response = {
            "message": "Task data updated successfully",
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
        }
        return jsonify(response), 200
    except Exception as e:
        db.rollback()
        response = {"error": f"Error updating task data: {str(e)}"}
        return jsonify(response), 500
    finally:
        cursor.close()


app.add_url_rule(routes["endpoint_edit_task"], "edit_task", edit_task, methods=["POST"])
