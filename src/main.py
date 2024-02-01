#!/usr/bin/env python3

from src.swagger.config import app
from src.endpoint.authentication.login import login
from src.endpoint.authentication.logout import logout
from src.endpoint.authentication.register import register
from src.endpoint.user.get_user import get_user
from src.endpoint.user.edit_user import edit_user
from src.endpoint.user.delete_user import delete_user
from src.endpoint.task.get_task import get_task
from src.endpoint.task.create_task import create_task
from src.endpoint.task.delete_task import delete_task
from src.endpoint.task.edit_task import edit_task

login
logout
register
get_user
edit_user
delete_user
get_task
create_task
delete_task
edit_task

if __name__ == "__main__":
    app.run(debug=True)
