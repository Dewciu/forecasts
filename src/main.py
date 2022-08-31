from re import S
from turtle import fd
import requests
import sys
from config.config_parser import Config
import logging
from common.init_module import Module

logging.basicConfig(level=logging.INFO)

def function_tee( *kwargs):
    print(kwargs)

if __name__ == "__main__":
    logging.info('Starting application')
    CONFIG = Config().get_config(sys.argv)

    Module(CONFIG).run()

    response = requests.get('http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/190390', params={'apikey':'ACEzczt5WrNJ4jTBN9XypvOQss6l02rl'})

    print(type(response.json()))

    function_tee({'hej':'test', 'hejo':'tescik'})

    str = '2022-08-31T18:00:00+00:00'

    print(str[11:19])