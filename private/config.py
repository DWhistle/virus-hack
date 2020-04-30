import yaml
import os
import logging.config
import logging
import copy


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
        print("RUNNING IN:", os.getenv("SERVER_MODE") or "DEV")
        if os.getenv("SERVER_MODE") == "PROD":
            conf_file = open("prod-config.yml", "r")
        else:
            conf_file = open("dev-config.yml", "r")
        config = yaml.safe_load(conf_file)
        cls.configure_logging(config['logging'])
        cls.db = cls.copy_config(config['postgres'])
        cls.app_config = cls.copy_config(config['flask'])
        conf_file.close()
