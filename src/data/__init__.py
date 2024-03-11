__all__ = ["init_db"]

import logging
from pymongo import MongoClient

from src.config import Config


def init_db() -> None:
    logger = logging.getLogger()

    logger.debug(f"Connecting to mongo on {Config.mongodb_host}:{Config.mongodb_port}")

    client: MongoClient = MongoClient(host=Config.mongodb_host, port=Config.mongodb_port)

    logger.debug("Successfully connected to mongo")

    databases = client.list_database_names()

    if "dashboard" not in databases:
        dashboard_db = client.get_database("dashboard")

        dashboard_db.create_collection("recipes")
