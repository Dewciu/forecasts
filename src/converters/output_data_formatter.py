from abc import ABC, abstractmethod
import converters.dataclasses_converters as dc


class SingleTypeOutputDataFormatter(ABC):

    sequence_type_key = 'sequence_type'
    base_time_key = 'base_time'
    component_key = 'component'
    forecast_data_key = 'forecast_data'
    rel_time_key = 'rel_time'
    data_key = 'data'

    @abstractmethod
    def _create_forecast_data_list(forecast_data: list) -> list:
        pass

    def get_formatted_data(self, component_data: list) -> list:
        formatted_data = []
        for component_set in component_data:
            dict_data = self._create_dict_of_single_component_string_data(
                component_set)
            formatted_data.append(dict_data)

        return formatted_data

    def _create_dict_of_single_component_string_data(self, component_set: dict) -> dict:
        sequence_type = component_set[self.sequence_type_key]
        base_time = component_set[self.base_time_key]
        rel_time = self._create_rel_time_string(
            component_set[self.forecast_data_key])
        data = self._create_forecast_data_string(
            component_set[self.forecast_data_key])

        return {self.component_key: component_set[self.component_key],
                "time_sequence": {
            f"@{self.sequence_type_key}": sequence_type,
            f"@{self.base_time_key}": base_time,
            f"@{self.rel_time_key}": rel_time,
            f"@{self.data_key}": data}
        }

    def _create_forecast_data_string(self, forecast_data: list) -> str:
        data = self._create_forecast_data_list(forecast_data)
        return self._create_converted_space_string(data)

    def _create_rel_time_string(self, forecast_data: list) -> str:
        rel_time_list = self._create_rel_time_list(forecast_data)
        return self._create_converted_space_string(rel_time_list)

    @staticmethod
    def _create_rel_time_list(forecast_data: list) -> list:
        rel_time_list = []
        for forecast in forecast_data:
            rel_time_list.append(forecast.time)

        return rel_time_list

    @staticmethod
    def _create_converted_space_string(data: list) -> str:
        ret_str = ''

        for item in data:
            ret_str += f" {str(item)}"

        return ret_str[1:]


class OutputTemperatureFormatter(SingleTypeOutputDataFormatter):

    @staticmethod
    def _create_forecast_data_list(forecast_data: list) -> list:
        forecast_data_list = []
        for forecast in forecast_data:
            forecast_data_list.append(forecast.temperature)

        return forecast_data_list


class FinalOutputDataFormatter:

    def __init__(self):
        self.component_key = 'component'
        self.time_sequence_key = 'time_sequence'

    def get_formatted_data(self, system: dc.System, forecast_data: list) -> dict:
        return self._create_system_output_dict(system, forecast_data)

    def _create_time_sequence_list_for_single_component(self, forecast_data: list) -> list:
        single_component_time_seq_list = []
        component_list = []
        for forecast in forecast_data:
            if forecast[self.component_key] not in component_list:
                component_list.append(forecast[self.component_key])

                dict_data = dict(component=forecast[self.component_key],
                                 time_sequence=[forecast[self.time_sequence_key]])
                single_component_time_seq_list.append(dict_data)
            else:
                for item in single_component_time_seq_list:
                    if item[self.component_key] == item:
                        item[self.time_sequence_key].append(forecast)

        if single_component_time_seq_list != []:
            return single_component_time_seq_list

    def _create_components_output_list(self, forecast_data: list) -> list:
        comp_output_list = []
        c_forecast_data = self._create_time_sequence_list_for_single_component(
            forecast_data)

        for component_set in c_forecast_data:
            single_comp_dict = {
                "@UID": component_set[self.component_key].uid,
                "model_parameters": {
                    "dynamic": {
                        "time_sequence": component_set[self.time_sequence_key]
                    }
                }
            }

            comp_output_list.append(single_comp_dict)

        if comp_output_list != []:
            return comp_output_list

    def _create_system_output_dict(self, system: dc.System, forecast_data: list) -> dict:
        component_list = self._create_components_output_list(forecast_data)

        return {
            "system": {
                "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "@UUID": system.uuid,
                "component": component_list
            }
        }
