import xmltodict


class XmlToDictConverter:
    """Converts raw XML data from the file, to Python dictionary."""

    def get_dict_from_file(self, file_path: str) -> dict:
        data = self._get_file_data(file_path)

        return self._convert_xml_to_dictionary(data)

    @staticmethod
    def _get_file_data(file_path: str) -> str:
        with open(file_path, 'r') as file:
            data = file.read()
        
        return data

    @staticmethod
    def _convert_xml_to_dictionary(data: str) -> dict:
        return xmltodict.parse(data, attr_prefix='')