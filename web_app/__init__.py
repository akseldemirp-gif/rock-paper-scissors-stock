"""Flask application factory."""

import os
import secrets

from dotenv import load_dotenv
from flask import Flask

from web_app.routes import home, rps, stocks


def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY") or secrets.token_hex(32),
        ALPHAVANTAGE_API_KEY=os.getenv("ALPHAVANTAGE_API_KEY", "").strip(),
        SESSION_COOKIE_SECURE=os.getenv("RENDER") == "true",
        SESSION_COOKIE_SAMESITE="Lax",
    )
    if test_config:
        app.config.update(test_config)

    app.register_blueprint(home)
    app.register_blueprint(rps)
    app.register_blueprint(stocks)
    return app
