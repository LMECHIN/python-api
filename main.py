#!/usr/bin/env python3

from swagger.config import app
from endpoint.login import login
from endpoint.logout import logout
from endpoint.register import register
from endpoint.user import user
from endpoint.edit_user import edit_user
from endpoint.delete_user import delete_user
from endpoint.create_task import create_task
from endpoint.get_task import get_task

login
logout
register
user
edit_user
delete_user
create_task
get_task

if __name__ == "__main__":
    app.run(debug=True)
