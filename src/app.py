__all__ = ["create_app"]

import logging
from logging import Logger
from sys import stdout

from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from src.config import Config
from src.data import init_db
from src.routes.api import api_bp
from src.routes.view import view_bp


def setup_logger(log_level: int) -> Logger:
    logger = logging.getLogger()
    logger.setLevel(log_level)
    stdout_handler = logging.StreamHandler(stdout)
    stdout_handler.setLevel(log_level)
    # file_handler = logging.FileHandler("dashboard.log")
    # file_handler.setLevel(log_level)

    formatter = logging.Formatter("%(name)s/%(levelname)s: %(message)s")
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    # logger.addHandler(file_handler)

    return logger


def create_app() -> Flask:
    logger = setup_logger(logging.NOTSET)
    Config.init()

    app = Flask(__name__)
    CORS(app)
    app.secret_key = Config.secret_key

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)  # type: ignore
    app.config.from_object(Config)

    app.register_blueprint(api_bp)
    app.register_blueprint(view_bp)

    for route in app.url_map.iter_rules():
        logger.debug(str(route))

    init_db()

    return app
