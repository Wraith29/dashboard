__all__ = ["Config"]

from dotenv import get_key, load_dotenv


class Config:
    _dotenv_path: str
    mongodb_port: int = 27017
    mongodb_host: str = "localhost"
    debug: bool = False

    @staticmethod
    def get_value(key: str) -> str:
        val = get_key(Config._dotenv_path, key)

        if val is None:
            raise KeyError(f"Key {key} not found in {Config._dotenv_path}")

        return val

    @staticmethod
    def init(debug: bool) -> None:
        Config._dotenv_path = ".env.dev" if debug else ".env"
        load_dotenv(Config._dotenv_path)

        Config.debug = debug
        Config.mongodb_port = int(Config.get_value("MONGODB_PORT"))
        Config.mongodb_host = Config.get_value("MONGODB_HOST")
