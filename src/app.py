__all__ = ["create_app"]

import logging
from os import getenv
from sys import stdout
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from src.config import Config
from src.data import init_db

from src.routes.api import api_bp
from src.routes.view import view_bp


def create_app() -> Flask:
    debug = True if int(getenv("FLASK_DEBUG", 0)) == 1 else False

    Config.init(debug)

    log_level = logging.NOTSET if Config.debug else logging.NOTSET

    logger = logging.getLogger()
    logger.setLevel(log_level)

    handler = logging.StreamHandler(stdout)
    handler.setLevel(log_level)

    formatter = logging.Formatter("%(name)s/%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    app = Flask(__name__)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)  # type: ignore
    app.config.from_object(Config)

    app.register_blueprint(api_bp)
    app.register_blueprint(view_bp)

    for route in app.url_map.iter_rules():
        logger.debug(str(route))

    init_db()

    return app
