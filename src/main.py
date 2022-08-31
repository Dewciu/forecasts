import requests
import pathlib
import bs4
import xmltodict
import pprint
import sys
import nested_lookup
from config.config_parser import Config

if __name__ == "__main__":

    CONFIG = Config().get_config(sys.argv)
    print(CONFIG)
