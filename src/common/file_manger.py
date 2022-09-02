from dataclasses import dataclass
import logging
from converters.xml_formatter import SystemXmlToDictConverter, DictToXmlConverter
from converters.dataclasses_converters import SystemDataclassConverter, System
import os
import glob

class SystemsXmlFileManager:
    
    def get_data(self, systems_path: str) -> list:
        if os.path.isdir(systems_path):
            return self._get_multiple_file_data(systems_path)
        elif os.path.isfile(systems_path):
            return self._get_single_file_data(systems_path)

    def save_data(self, system: System, data: dict, output_base_path: str):
        xml_data = self._get_xml_data_from_dictionary(data)
        filename = self._get_filename(system)

        with open(f"{output_base_path}/{filename}", 'w') as file:
            file.write(xml_data)

        logging.info(f"Saved file {output_base_path}/{filename}")

    @staticmethod
    def _get_filename(system: System) -> str:
        input_filename = system.filename
        output_filename = input_filename.replace('.xml','') + '_forecast.xml'
        return output_filename

    @staticmethod
    def _get_xml_data_from_dictionary(data: dict) -> str:
        return DictToXmlConverter().get_xml_string_from_dictionary(data)

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
        return SystemDataclassConverter().convert(system)[0]

    @staticmethod
    def _get_list_of_file_paths(directory: str) -> list:
        return glob.glob(f"{directory}/*.xml")