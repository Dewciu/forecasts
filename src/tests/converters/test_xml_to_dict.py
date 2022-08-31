from converters.xml_to_dict import XmlToDictConverter
from tests.converters.data import DICT_XML_DATA

path = '/Users/dewciu/Development/private/krypton_polska_zadanie/systems/system1.xml'

with open(path, 'r') as file:
    data = file.read()


def test_get_file_data():
    assert XmlToDictConverter._get_file_data(path) == data

def test_xml_to_dictionary_conversion():
    assert XmlToDictConverter._convert_xml_to_dictionary(data) == DICT_XML_DATA