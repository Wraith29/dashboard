__all__ = ["Config"]

from enum import Enum
from logging import getLogger
from tomllib import load
from typing import TypedDict


class EnvironmentMode(Enum):
    debug = "debug"
    prod = "prod"


class Environment(TypedDict):
    mode: EnvironmentMode
    port: int


class MongoSettings(TypedDict):
    port: int
    host: str


class SpotifySettings(TypedDict):
    state: str
    client_id: str
    client_secret: str
    redirect_uri: str


class SetlistSettings(TypedDict):
    api_key: str


class Config:
    environment: Environment
    secret_key: str
    mongo: MongoSettings
    spotify: SpotifySettings
    setlist: SetlistSettings

    @staticmethod
    def init() -> None:
        logger = getLogger()
        cfg_path = "config/settings.toml"

        logger.debug(f"Loading Config from {cfg_path}")

        cfg_file = open(cfg_path, "rb")

        cfg = load(cfg_file)

        Config.environment = cfg["environment"]
        Config.secret_key = cfg["secret-key"]
        Config.mongo = cfg["mongo"]
        Config.spotify = cfg["spotify"]
        Config.setlist = cfg["setlist"]

        cfg_file.close()
