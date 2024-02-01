from flask import jsonify, g
from flasgger import swag_from
from src.swagger.config import app
from src.authenticate.auth import requires_auth
import src.authenticate.connect_db as connect_db

db = connect_db.db()
routes = connect_db.routes()


@swag_from(routes["swagger_get_task"])
@requires_auth
def get_task():
    user_id = g.user.get("id")
    cursor = None

    try:
        cursor = db.cursor()
        query = "SELECT * FROM tasks WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        tasks = cursor.fetchall()

        task_list = []
        for task in tasks:
            task_dict = {
                "task_id": task[0],
                "user_id": task[1],
                "title": task[2],
                "description": task[3],
                "due_date": task[4],
                "status": task[5],
                "priority": task[6],
                "created_at": task[7],
                "updated_at": task[8],
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


app.add_url_rule(routes["endpoint_get_task"], "get_task", get_task, methods=["GET"])
