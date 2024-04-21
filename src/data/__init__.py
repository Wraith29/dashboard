__all__ = ["init_db"]

import logging
from typing import Any
from pymongo import MongoClient

from src.config import Config


def init_db() -> None:
    logger = logging.getLogger()

    logger.debug("Connecting to mongo on '%s:%s'", Config.mongo["host"], Config.mongo["port"])

    client: MongoClient[Any] = MongoClient(host=Config.mongo["host"], port=Config.mongo["port"])

    logger.debug("Successfully connected to mongo")

    databases = client.list_database_names()

    if "dashboard" not in databases:
        dashboard_db = client.get_database("dashboard")

        dashboard_db.create_collection("recipes")
