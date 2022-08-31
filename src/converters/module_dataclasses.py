import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, is_dataclass


@dataclass
class System:
    filename: str
    uuid: str
    components: list
    update_period: int = None

    def __repr__(self):
        return f"SYSTEM: (filename: {self.filename}, uuid: {self.uuid}, comp_count: {len(self.components)}, update_period: {self.update_period})"


@dataclass
class Component:
    base_system_uuid: str
    uid: str
    latitude: str
    longitude: str
    name: str


@dataclass
class ComponentTemperature:
    component: Component
    time: str
    temperature: int
    unit: str

    def __post_init__(self):
        if self.unit == 'F':
            self.temperature = (self.temperature-32)/1.8
            self.unit = 'C'


class DataclassConverter(ABC):

    @abstractmethod
    def convert(self) -> list:
        """Main conversion method, which returns list of specific dataclasses."""
        pass

    @abstractmethod
    def _convert_from_dict(self) -> dataclass:
        """Should return dataclass from a specific dictionary."""
        pass

    @abstractmethod
    def _convert_from_list(self) -> list:
        """Should return a list with specific dataclasses. Best use with _convert_from_dict method."""
        pass


class SystemDataclassConverter(DataclassConverter):
    """Converts system dictionary to system dataclass"""

    def __init__(self):
        self.dataclass = System
        self.system_key = 'system'
        self.uuid_key = 'UUID'
        self.components_key = 'component'
        self.update_period_key = 'update_period'
        self.filename_key = 'filename'

    def convert(self, systems) -> list:
        ret_list = []

        if isinstance(systems, list):
            ret_list.extend(self._convert_from_list(systems))
        elif isinstance(systems, dict):
            ret_list.append(self._convert_from_dict(systems))

        if ret_list != []:
            return ret_list

    def _convert_from_dict(self, system: dict) -> dataclass:
        try:
            concrete_system = system[self.system_key]

            filename = concrete_system[self.filename_key]
            uuid = concrete_system[self.uuid_key]
            components = concrete_system[self.components_key]
            update_period = self._get_update_period(concrete_system)

            return self.dataclass(filename, uuid, components, update_period)
        except KeyError as key:
            logging.error(
                f'Invalid key ({key}) in dictionary, cannot convert to dataclass')

    def _convert_from_list(self, systems: list) -> list:
        ret_list = []
        for system in systems:
            ret_list.append(self._convert_from_dict(system))

        return ret_list

    def _get_update_period(self, system: dict) -> int:
        if self.update_period_key in system.keys():
            try:
                update_period = int(system[self.update_period_key])
                return update_period
            except ValueError:
                logging.error(
                    f"Update period should be integer or integer string, actual value: {system[self.update_period_key]}")


class ComponentDataclassConverter(DataclassConverter):
    """Converts component data from system dataclass to the list of components dataclass"""

    def __init__(self):
        self.component_dataclass = Component
        self.uid_key = 'UID'
        self.latitude_key = 'latitude'
        self.longitude_key = 'longitude'
        self.name_key = 'name'

    def convert(self, system: System) -> list:
        if is_dataclass(system):
            return self._convert_from_dict_or_list(system.uuid, system.components)

    def _convert_from_dict_or_list(self, base_system_uuid, components) -> list:
        ret_list = []

        if isinstance(components, list):
            ret_list.extend(self._convert_from_list(
                base_system_uuid, components))
        elif isinstance(components, dict):
            ret_list.append(self._convert_from_dict(
                base_system_uuid, components))

        if ret_list != []:
            return ret_list

    def _convert_from_dict(self, bs_uuid: str, component: dict) -> dataclass:
        try:

            base_system_uuid = bs_uuid
            uid = component[self.uid_key]
            latitude = component[self.latitude_key]
            longitude = component[self.longitude_key]
            name = component[self.name_key]

            return self.component_dataclass(base_system_uuid, uid, latitude, longitude, name)

        except KeyError as key:
            logging.error(
                f'Invalid key ({key}) in dictionary, cannot convert to dataclass')

    def _convert_from_list(self, base_system_uuid: str, components: list) -> list:
        ret_list = []
        for component in components:
            ret_list.append(self._convert_from_dict(
                base_system_uuid, component))

        return ret_list


class ComponentTemperatureDataclassConverter(DataclassConverter):

    def __init__(self):
        self.comp_temp_dataclass = ComponentTemperature
        self.temp_key = 'Temperature'
        self.temp_val_key = 'Value'
        self.temp_unit_key = 'Unit'
        self.date_time_key = 'DateTime'

    def convert(self, component: Component, temperature) -> list:
        ret_list = []
        if isinstance(temperature, list):
            ret_list.extend(self._convert_from_list(component, temperature))
        elif isinstance(temperature, dict):
            ret_list.append(self._convert_from_dict(component, temperature))

    def _convert_from_dict(self, comp: Component, temp: dict) -> dataclass:
        try:
            component = comp
            time = self._get_proper_time(temp[self.date_time_key])
            temperature = int(temp[self.temp_key][self.temp_val_key])
            unit = temp[self.temp_key][self.temp_unit_key]

            return self.comp_temp_dataclass(component, time, temperature, unit)

        except KeyError as key:
            logging.error(
                f'Invalid key ({key}) in dictionary, cannot convert to dataclass')

    def _convert_from_list(self, component: Component, temperature: list) -> list:
        ret_list = []
        for temp in temperature:
            ret_list.append(self._convert_from_dict(component, temp))

        return ret_list

    @staticmethod
    def _get_proper_time(time):
        return time[11:19]
