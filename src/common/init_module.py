import logging
import time
from threading import Thread

from converters.dataclasses_converters import System
from converters.output_data_formatter import FinalOutputDataFormatter

from common.file_manger import SystemsXmlFileManager
from common.forecasts_managers import TemperatureManagerCreator


class Module:

    """
    Main Module which chooses a mode, and then mainatins specific modes.
    """

    def __init__(self, config: dict):
        
        """
        In forecast_managers can define specific forecast manager creator which will handle seprate weather parameter type,
        like temperature, clouds, rain etc.
        """

        self.output_path = config['output_path']
        self.mode = config['mode']
        self.systems = SystemsXmlFileManager().get_data(config['entry_path'])
        self.forecasts_managers = [
            TemperatureManagerCreator(config['api_key'])
        ]

    def run(self):
        if self.mode == 'single_time':
            self._single_run()
        elif self.mode == 'continous':
            self._continous_run()

    def _single_run(self):
        for system in self.systems:
            self._get_data_and_save_to_file(system)

    def _continous_run(self):
        threads = []
        for system in self.systems:

            thread = Thread(target=self._create_loop, args=(system,))
            threads.append(thread)
            thread.start()

    def _get_data(self, system: System) -> dict:
        forecast_data = []

        for manager in self.forecasts_managers:
            data = manager.get_data_for_system(system)
            if data is not None:
                forecast_data.extend(data)

        return FinalOutputDataFormatter().get_formatted_data(system, forecast_data)

    def _get_data_and_save_to_file(self, system: System):
        data = self._get_data(system)
        SystemsXmlFileManager().save_data(system, data, self.output_path)

    def _create_loop(self, system: System):

        update_period = system.update_period

        if update_period is None:
            update_period = 60

        logging.info(
            f"Starting loop for file: {system.filename}, update_period: {update_period} sec.")

        while True:
            self._get_data_and_save_to_file(system)

            time.sleep(update_period)
