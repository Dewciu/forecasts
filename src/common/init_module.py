import os
from common.file_manger import SystemsFileManager

class Module:

    def __init__(self, config: dict):
        self.entry_path = config['entry_path']
        self.output_path = config['output_path']
        self.mode = config['mode']
        self.api_key = config['api_key']

    def run(self):
        if self.mode == 'single_time':
            self._single_run()
        elif self.mode == 'continous':
            self._continous_run()

    def _single_run(self):
        print(SystemsFileManager().get_data(self.entry_path))

    def _continous_run(self):
        pass