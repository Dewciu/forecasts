from tests.converters.data import DICT_XML_DATA_PERIOD, LIST_XML_DATA, DICT_XML_DATA_INVALID_PERIOD
from converters.module_dataclasses import System, SystemDataclassConverter, ComponentDataclassConverter, Component
import pytest
from dataclasses import asdict


def test_system_conversion_get_period():
    assert SystemDataclassConverter()._get_update_period(
        DICT_XML_DATA_PERIOD['system']) == 20


def test_system_conversion_with_update_period_dict():

    components = DICT_XML_DATA_PERIOD['system']['component']
    uuid = DICT_XML_DATA_PERIOD['system']['UUID']
    filename = 'system1.xml'

    system_list = [System(filename=filename,
                          uuid=uuid,
                          components=components, update_period=20)]

    assert SystemDataclassConverter().convert(DICT_XML_DATA_PERIOD) == system_list


def test_system_conversion_list():

    components1 = LIST_XML_DATA[0]['system']['component']
    components2 = LIST_XML_DATA[1]['system']['component']

    uuid1 = LIST_XML_DATA[0]['system']['UUID']
    uuid2 = LIST_XML_DATA[1]['system']['UUID']

    filename1 = 'system1.xml'
    filename2 = 'system2.xml'

    system_list = [System(filename=filename1,
                          uuid=uuid1,
                          components=components1, update_period=20), System(
        filename=filename2, uuid=uuid2,
        components=components2, update_period=None)]

    assert SystemDataclassConverter().convert(LIST_XML_DATA) == system_list


def test_component_conversion():
    components = DICT_XML_DATA_PERIOD['system']['component']
    uuid = DICT_XML_DATA_PERIOD['system']['UUID']
    update_period = DICT_XML_DATA_PERIOD['system']['update_period']
    filename = 'system1.xml'

    system = System(filename, uuid, components, update_period)

    components_dataclasses = [
        Component(DICT_XML_DATA_PERIOD['system']['UUID'],
                  components[0]['UID'],
                  components[0]['latitude'],
                  components[0]['longitude'],
                  components[0]['name']),
        Component(DICT_XML_DATA_PERIOD['system']['UUID'],
                  components[1]['UID'],
                  components[1]['latitude'],
                  components[1]['longitude'],
                  components[1]['name']),
        Component(DICT_XML_DATA_PERIOD['system']['UUID'],
                  components[2]['UID'],
                  components[2]['latitude'],
                  components[2]['longitude'],
                  components[2]['name'])
    ]

    components_converted = ComponentDataclassConverter().convert(system)

    for index, component in enumerate(components_converted):
        assert components_converted[index] == components_dataclasses[index]
