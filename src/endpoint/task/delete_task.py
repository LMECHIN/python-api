from flask import request, jsonify, g
from flasgger import swag_from
from src.swagger.config import app
from src.authenticate.auth import requires_auth
import src.authenticate.connect_db as connect_db

db = connect_db.db()
routes = connect_db.routes()


@swag_from(routes["swagger_delete_task"])
@requires_auth
def delete_task():
    user_id = g.user.get("id")

    if request.headers["Content-Type"] == "application/json":
        data = request.json
        task_id = data.get("task_id")
    else:
        data = request.form
        task_id = data.get("task_id")

    if not task_id:
        response = {"error": "Task ID not provided"}
        return jsonify(response), 400

    cursor = None
    try:
        cursor = db.cursor()
        query = "DELETE FROM tasks WHERE user_id = %s AND task_id = %s;"
        cursor.execute(query, (user_id, task_id))
        db.commit()

        response = {"message": "Task deleted successfully"}
        return jsonify(response)

    except Exception as e:
        db.rollback()
        response = {"error": f"Error deleting task: {str(e)}"}
        return jsonify(response), 500

    finally:
        cursor.close()


app.add_url_rule(
    routes["endpoint_delete_task"], "delete_task", delete_task, methods=["DELETE"]
)
