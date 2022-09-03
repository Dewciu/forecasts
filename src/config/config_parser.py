from os import path
from pathlib import Path

from converters.xml_formatter import XmlToDictConverter

import config.exceptions as exc


class Config:
    """Command line initialization arguments validator"""

    def __init__(self):
        self.init_args = None
        self.valid_modes = ['-c', '-s']
        self.absolute_path = str(Path().resolve()).replace('/src', '')
        self.api_key_path = f"{self.absolute_path}/api_keys/api_key.xml"

    def get_config(self, args: list) -> dict:
        if self._is_valid(args):
            return self._convert_to_dictionary(args)

    def _convert_to_dictionary(self, args: list) -> dict:
        entry_path = self._get_full_path(args[1])
        output_path = self._get_full_path(args[2])
        mode = self._get_mode_name(args[3])
        api_key = self._get_api_key()['api_key']['key']

        return dict(entry_path=entry_path, output_path=output_path, mode=mode, api_key=api_key)

    def _get_full_path(self, folder: str) -> str:
        return f"{self.absolute_path}/{folder}"

    def _is_valid(self, args: list) -> bool:
        if self._args_count_is_valid(args) and self._mode_and_path_is_valid(args):
            return True

    def _mode_and_path_is_valid(self, args: list) -> bool:
        if self._entry_file_path_exists(args[1]) and self._mode_is_valid(args[3], self.valid_modes):
            return True

    def _entry_file_path_exists(self, path_arg: str) -> bool:

        entry_file_path = f'{self.absolute_path}/{path_arg}'

        if path.exists(entry_file_path):
            return True
        else:
            raise exc.InitArgsPathNotExists(entry_file_path)

    def _get_api_key(self):
        return XmlToDictConverter().get_dict_from_file(self.api_key_path)

    @staticmethod
    def _mode_is_valid(mode: str, valid_modes: list) -> bool:
        if mode in valid_modes:
            return True
        else:
            raise exc.InitArgsInvalidModeType(mode, valid_modes)

    @staticmethod
    def _args_count_is_valid(args: list) -> bool:
        if len(args) != 4:
            raise exc.InitArgsCountError(args)
        else:
            return True

    @staticmethod
    def _get_mode_name(mode: str) -> bool:
        if mode == '-c':
            return 'continous'
        elif mode == '-s':
            return 'single_time'
