from dataclasses import dataclass

@dataclass
class System:
    uuid: str
    components: list

@dataclass
class Component:
    uid: str
    latitude: str
    longitude: str
    name: str

class SystemDataclassConverter:
    
    def __init__(self):
        self.dataclass = System

    def convert(self, data: dict) -> list:
        pass

    def _convert_from_dict(self):
        pass

    def _convert_from_list(self):
        pass