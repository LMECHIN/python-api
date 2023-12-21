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
