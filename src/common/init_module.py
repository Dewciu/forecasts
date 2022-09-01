import os
from common.file_manger import SystemsFileManager
from common.forecasts_managers import TemperatureManagerCreator

class Module:

    def __init__(self, config: dict):
        self.output_path = config['output_path']
        self.mode = config['mode']
        self.systems = SystemsFileManager().get_data(config['entry_path'])
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
            # print(self.forecasts_managers[0].get_data_for_system(system))
            pass


    def _continous_run(self):
        pass