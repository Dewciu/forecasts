import requests
import pathlib
import bs4
import xmltodict
import pprint
import sys
import nested_lookup
from config.config_parser import Config
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    logging.info('Starting application')
    CONFIG = Config().get_config(sys.argv)