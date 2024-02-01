from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
app.config["SWAGGER"] = {"title": "My API", "uiversion": 3}
template = {
    "swagger": "2.0",
    "info": {
        "title": "PYTHON API",
        "description": "API for my data",
        "version": "0.0.1",
    },
    # "host": "http://127.0.0.1:5000",
}

config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/",
}
swagger = Swagger(app, template=template, config=config)
