from abc import ABC, abstractmethod
from datetime import datetime

import converters.dataclasses_converters as dc
import converters.output_data_formatter as odf
import weather_requests.request as req


class ForecastManager:

    """
    Base forecast manager, which is a base class for specific
    forecast managers like temperature manager or rain manager.
    There is a need to set class values like:
    
    forecast_req - request class which should inherit interface from RequestCreator,
    forecasts_converter - specific dataclass converter which should inherit from DataclassConverter,
    output_formatter - specific output formatter which should inherit from SingleTypeOutputDataFormatter,
    req_api_key - api key parsed from config values, which should be provided from ./api_keys/ path,
    sequence_type_name - string name of specific forecast, for example - 'temperature' or 'rain'
    """

    forecast_req: req.RequestCreator = None
    forecasts_converter: dc.DataclassConverter = None
    output_formatter: odf.SingleTypeOutputDataFormatter = None
    req_api_key: str = None
    sequence_type_name: str = None

    def __init__(self):
        self.system = None
        self.component_converter = dc.ComponentDataclassConverter()
        self.geoposition_req = req.AccuWeatherGeopositionRequest()
        self.geoposition_resp_id_key = 'Key'

    def get_data(self, system: dc.System):
        """Get data interface for getting formatted forecast data, ready to be converted by output converter."""
        self.system = system

        return self._get_output_formatted_data()

    def _get_output_formatted_data(self):
        component_data = self._get_forecast_data_for_all_components()
        if component_data is not None:
            flat_comp_list = [
                component for sublist in component_data for component in sublist]
            return self.output_formatter.get_formatted_data(flat_comp_list)

    def _get_component_list(self) -> list:
        return self.component_converter.convert(self.system)

    def _get_localization_key(self, component: dc.Component) -> str:
        geo_position = self._get_converted_geoposition(component)
        data = self.geoposition_req.get_data(self.req_api_key, geo_position)

        if data is not None:
            return data[self.geoposition_resp_id_key]

    def _get_single_localization_component_set(self) -> list:
        ret_key_comp_list = []
        key_list = []

        components = self._get_component_list()

        for component in components:
            key = self._get_localization_key(component)

            if key:
                if key not in key_list:
                    key_list.append(key)
                    ret_key_comp_list.append(
                        dict(loc_key=key, components=[component]))
                else:
                    for item in ret_key_comp_list:
                        if item['loc_key'] == key:
                            item['components'].append(component)

        if ret_key_comp_list != []:
            return ret_key_comp_list

    def _get_forecast_data_for_all_components(self) -> list:
        forecast_data = []

        component_set = self._get_single_localization_component_set()

        if component_set:
            for comp_set in component_set:
                forecast_data.append(
                    self._get_forecast_data_for_single_component_set(comp_set))

            return forecast_data

    def _get_forecast_data_for_single_component_set(self, comp_set: dict) -> list:
        data = self.forecast_req.get_data(
            self.req_api_key, comp_set['loc_key'])

        return self._get_forecast_data(data, comp_set)

    def _get_forecast_data(self, data: list, comp_set: dict) -> list:
        ret_forecast_data_list = []

        if data is not None:
            for component in comp_set['components']:

                forecast_data = self.forecasts_converter.convert(data)

                ret_forecast_data_list.append(dict(sequence_type=self.sequence_type_name,
                                                   base_time=self._get_base_time(),
                                                   component=component,
                                                   forecast_data=forecast_data))

            return ret_forecast_data_list

    @staticmethod
    def _get_converted_geoposition(component: dc.Component):
        return f"{component.latitude},{component.longitude}"

    @staticmethod
    def _get_base_time():
        base_time = datetime.now()
        return base_time.strftime("%Y-%m-%dT%H%:%M:%S")


class ForecastManagerCreator(ABC):

    """
    Base forecast manager creator which sets specific parameters for base ForecastManager class.
    All specific ForecastManagersCreators should provide all abstractmethod."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    def factory_method(self) -> ForecastManager:
        """Should return specific forecast manager class."""
        return ForecastManager()

    @abstractmethod
    def _get_specific_forecast_dataclass_converter(self) -> dc.DataclassConverter:
        """Should return specific forecast dataclass converter, like temperature converter
        or rain converter."""
        return dc.DataclassConverter()

    @abstractmethod
    def _get_forecast_request_class(self) -> req.RequestCreator:
        """Should return request class for specific forecast."""
        return req.RequestCreator()

    @abstractmethod
    def _get_sequence_type_name(self) -> str:
        """Should return string with name of specific sequence, like: 'temperature' or 'rain'"""
        return ''

    @abstractmethod
    def _get_single_type_output_data_formatter(self) -> odf.SingleTypeOutputDataFormatter:
        """Should return single type output data formatter class."""
        return odf.SingleTypeOutputDataFormatter()

    def get_data_for_system(self, system: dc.System):
        forecast_manager = self._get_configured_forecast_manager()
        return forecast_manager.get_data(system)

    def _get_configured_forecast_manager(self) -> ForecastManager:
        """Setting all credentials for specific forecast manager."""

        forecast_manager = self.factory_method()
        forecast_manager.forecast_req = self._get_forecast_request_class()
        forecast_manager.forecasts_converter = self._get_specific_forecast_dataclass_converter()
        forecast_manager.output_formatter = self._get_single_type_output_data_formatter()
        forecast_manager.req_api_key = self.api_key
        forecast_manager.sequence_type_name = self._get_sequence_type_name()

        return forecast_manager


class TemperatureManager(ForecastManager):
    """Specific temperature manager class"""
    pass

class DaylightManager(ForecastManager):
    pass

class TemperatureManagerCreator(ForecastManagerCreator):

    def factory_method(self) -> ForecastManager:
        return TemperatureManager()

    def _get_specific_forecast_dataclass_converter(self) -> dc.DataclassConverter:
        return dc.AccuWeatherComponentTemperatureDataclassConverter()

    def _get_forecast_request_class(self) -> req.RequestCreator:
        return req.AccuWeather12HoursForecastsRequest()

    def _get_sequence_type_name(self) -> str:
        return 'temperature'

    def _get_single_type_output_data_formatter(self) -> odf.SingleTypeOutputDataFormatter:
        return odf.OutputTemperatureFormatter()

class DaylightManagerCreator(ForecastManagerCreator):

    def factory_method(self) -> ForecastManager:
        return DaylightManager()

    def _get_specific_forecast_dataclass_converter(self) -> dc.DataclassConverter:
        return dc.AccuWeatherComponentDaylightDataclassConverter()

    def _get_forecast_request_class(self) -> req.RequestCreator:
        return req.AccuWeather12HoursForecastsRequest()

    def _get_sequence_type_name(self) -> str:
        return 'day_light'

    def _get_single_type_output_data_formatter(self) -> odf.SingleTypeOutputDataFormatter:
        return odf.OutputDaylightFormatter()