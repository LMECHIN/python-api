#!/usr/bin/env python3

from swagger.config import app
from endpoint.login import login
from endpoint.register import register
from endpoint.user import user

login
register
user

if __name__ == "__main__":
    app.run(debug=True)
