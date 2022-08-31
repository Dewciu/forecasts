from converters.xml_to_dict import XmlToDictConverter, SystemXmlToDictConverter
from tests.converters.data import DICT_XML_DATA, DICT_XML_DATA_WITH_FILE

path = '/Users/dewciu/Development/private/krypton_polska_zadanie/systems/system1.xml'

with open(path, 'r') as file:
    data = file.read()


def test_get_file_data():
    assert XmlToDictConverter._get_file_data(path) == data

def test_system_xml_to_dictionary_conversion():

    c_data = SystemXmlToDictConverter().get_dict_from_file(path)
    assert c_data == DICT_XML_DATA_WITH_FILE


def test_xml_to_dictionary_conversion():
    assert XmlToDictConverter._convert_xml_to_dictionary(data) == DICT_XML_DATA

