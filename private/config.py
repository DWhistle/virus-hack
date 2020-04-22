import yaml
import os
import logging.config
import logging


def configure_logging(config: dict):
    logging.config.dictConfig(config)


def configure_resources():
    print("RUNNING IN:", os.getenv("SERVER_MODE") or "DEV")
    if os.getenv("SERVER_MODE") == "PROD":
        conf_file = open("prod-config.yml", "r")
    else:
        conf_file = open("dev-config.yml", "r")
    config = yaml.safe_load(conf_file)
    configure_logging(config['logging'])
    conf_file.close()
