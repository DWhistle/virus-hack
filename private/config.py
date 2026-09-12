"""Mode-specific logging plus validated environment-only runtime configuration."""
import copy
import logging.config
import os
from pathlib import Path

import yaml


class Configurator:
    app_config = None
    db = None

    @classmethod
    def configure_logging(cls, config: dict):
        logging.config.dictConfig(config)

    @staticmethod
    def copy_config(config: dict):
        return copy.deepcopy(config)

    @classmethod
    def configure_resources(cls):
        mode = os.environ.get("SERVER_MODE", "DEV")
        if mode not in {"DEV", "PROD"}:
            raise ValueError("SERVER_MODE must be DEV or PROD")
        required = ["DB_USER", "DB_PASSWORD", "DB_NAME", "FLASK_SECRET"]
        if mode == "PROD":
            required += ["DB_HOST", "IMAGES_FOLDER"]
        missing = [name for name in required if not os.environ.get(name, "").strip()]
        if missing:
            raise ValueError("Missing required environment variables: " + ", ".join(missing))
        try:
            port = int(os.environ.get("DB_PORT", "5432"))
            if not 1 <= port <= 65535:
                raise ValueError
        except ValueError:
            raise ValueError("DB_PORT must be an integer between 1 and 65535") from None
        if len(os.environ["FLASK_SECRET"]) < 32:
            raise ValueError("FLASK_SECRET must contain at least 32 characters")
        root = Path(__file__).resolve().parent.parent
        with (root / f"{mode.lower()}-config.yml").open() as stream:
            config = yaml.safe_load(stream)
        cls.configure_logging(config["logging"])
        cls.db = {
            "driver": "postgresql+psycopg2",
            "host": os.environ.get("DB_HOST", "127.0.0.1"),
            "port": port,
            "user": os.environ["DB_USER"],
            "password": os.environ["DB_PASSWORD"],
            "database": os.environ["DB_NAME"],
        }
        cls.app_config = {
            "secret": os.environ["FLASK_SECRET"],
            "images_folder": os.environ.get("IMAGES_FOLDER", str(root / "pictures")),
        }
