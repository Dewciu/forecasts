from abc import ABC, abstractmethod
import converters.dataclasses_converters as dc


class OutputDataFormatter(ABC):

    def __init__(self):
        self.component_key = 'component'
        self.forecast_data_key = 'forecast_data'

    @abstractmethod
    @staticmethod
    def _get_forecast_data_list(self, forecast_data: list) -> list:
        pass

    def get_formatted_data(self, system: dc.System, component_data: list):
        pass

    def _get_data_for_single_component(self, component_data: list) -> dict:
        for component in component_data:
            pass

    def _get_forecast_data_string(self, forecast_data: list) -> str:
        data = self._get_forecast_data_list(forecast_data)
        return self._get_converted_space_string(data)

    def _get_rel_time_string(self, forecast_data: list) -> str:
        rel_time_list = self._get_rel_time_list(forecast_data)
        return self._get_converted_space_string(rel_time_list)

    @staticmethod
    def _get_rel_time_list(forecast_data:list) -> list:
        rel_time_list = []
        for forecast in forecast_data:
            rel_time_list.append(forecast.time)

        return rel_time_list

    @staticmethod
    def _get_converted_space_string(data: list) -> str:
        ret_str = ''

        for item in data:
            ret_str += f" {str(item)}"

        return ret_str[1:]

class OutputTemperatureFormatter(OutputDataFormatter):
    
    @staticmethod
    def _get_forecast_data_list(forecast_data: list) -> list:
        forecast_data_list = []
        for forecast in forecast_data:
            forecast_data_list.append(forecast.temperature)
        
        return forecast_data_list
