import logging
import sys

from common.init_module import Module
from config.config_parser import Config

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info('Starting application')
    CONFIG = Config().get_config(sys.argv)

    Module(CONFIG).run()
