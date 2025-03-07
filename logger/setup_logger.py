import logging.config

import yaml


def setup_logger():
    with open(file="logger/config.yaml", mode="rt") as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config)
