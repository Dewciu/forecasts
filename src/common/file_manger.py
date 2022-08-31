from dataclasses import dataclass
from genericpath import isdir, isfile
from converters.xml_to_dict import SystemXmlToDictConverter
from converters.module_dataclasses import SystemDataclassConverter
import os
import glob

class SystemsFileManager:
    
    def get_data(self, systems_path: str) -> list:
        if os.path.isdir(systems_path):
            return self._get_multiple_file_data(systems_path)
        elif os.path.isfile(systems_path):
            return self._get_single_file_data(systems_path)

    def _get_single_file_data(self, file_path: str):
        system = SystemXmlToDictConverter().get_dict_from_file(file_path)
        
        return self._get_system_as_dataclass(system)

    def _get_multiple_file_data(self, directory: str):
        files = self._get_list_of_file_paths(directory)
        system_data = []

        for file in files:
            system_data.append(self._get_single_file_data(file))

        return system_data

    @staticmethod
    def _get_system_as_dataclass(system: dict) -> dataclass:
        return SystemDataclassConverter().convert(system)

    @staticmethod
    def _get_list_of_file_paths(directory: str) -> list:
        return glob.glob(f"{directory}/*.xml")