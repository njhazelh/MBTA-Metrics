import logging
from mbtaalerts.config import directed_config as cfg

logging.basicConfig(format=cfg.get('Logging', 'format'),
                    datefmt=cfg.get('Logging', 'datefmt'),
                    level=cfg.get('Logging', 'level'))

def get_log(name):
    return logging.getLogger(name)
