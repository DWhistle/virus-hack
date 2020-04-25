import yaml
import os
import logging.config
import logging
import copy

db = None

def configure_logging(config: dict):
    logging.config.dictConfig(config)

def configure_db(config: dict):
    return copy.deepcopy(config)

def configure_resources():
    global db
    print("RUNNING IN:", os.getenv("SERVER_MODE") or "DEV")
    if os.getenv("SERVER_MODE") == "PROD":
        conf_file = open("prod-config.yml", "r")
    else:
        conf_file = open("dev-config.yml", "r")
    config = yaml.safe_load(conf_file)
    configure_logging(config['logging'])
    db = configure_db(config['postgres'])
    conf_file.close()
