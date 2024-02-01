import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def db():
    db_config = {
        "host": os.getenv("HOST"),
        "user": os.getenv("USER_HOST"),
        "password": os.getenv("PASSWORD"),
        "database": os.getenv("DATABASE"),
    }

    connection = mysql.connector.connect(**db_config)

    return connection


def routes():
    routes_config = {
        "endpoint_login": os.getenv("ENDPOINT_LOGIN"),
        "swagger_login": os.getenv("SWAGGER_LOGIN"),
        "endpoint_logout": os.getenv("ENDPOINT_LOGOUT"),
        "swagger_logout": os.getenv("SWAGGER_LOGOUT"),
        "endpoint_register": os.getenv("ENDPOINT_REGISTER"),
        "swagger_register": os.getenv("SWAGGER_REGISTER"),
        "endpoint_create_task": os.getenv("ENDPOINT_CREATE_TASK"),
        "swagger_create_task": os.getenv("SWAGGER_CREATE_TASK"),
        "endpoint_delete_task": os.getenv("ENDPOINT_DELETE_TASK"),
        "swagger_delete_task": os.getenv("SWAGGER_DELETE_TASK"),
        "endpoint_edit_task": os.getenv("ENDPOINT_EDIT_TASK"),
        "swagger_edit_task": os.getenv("SWAGGER_EDIT_TASK"),
        "endpoint_get_task": os.getenv("ENDPOINT_GET_TASK"),
        "swagger_get_task": os.getenv("SWAGGER_GET_TASK"),
        "endpoint_delete_user": os.getenv("ENDPOINT_DELETE_USER"),
        "swagger_delete_user": os.getenv("SWAGGER_DELETE_USER"),
        "endpoint_edit_user": os.getenv("ENDPOINT_EDIT_USER"),
        "swagger_edit_user": os.getenv("SWAGGER_EDIT_USER"),
        "endpoint_get_user": os.getenv("ENDPOINT_GET_USER"),
        "swagger_get_user": os.getenv("SWAGGER_GET_USER"),
    }

    if routes_config is None:
        print(f"Error: failed to load .env: {routes_config}")
        return

    return routes_config
