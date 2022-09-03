import logging
from abc import ABC, abstractmethod

import requests
from requests.adapters import HTTPAdapter


class Request:

    """Base request class which returns data for specific endpoint and params set in credentials."""

    def __init__(self):
        self.url: str = None
        self.request_params = None
        self.error_status_codes: list = None

    def set_credentials(self, url, error_status_codes: list, **kwargs):
        """Sets the url, possible error status codes and kwargs for specific params.
        key in kwargs means param, and value means value of the param."""

        self.url = url
        self.request_params = kwargs
        self.error_status_codes = error_status_codes

    def get_data(self):
        return self._get_request_data()

    def _get_request_data(self):
        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=2))

        try:
            response = session.get(self.url, params=self.request_params)
            if self._proper_status_code(response):
                return response.json()

        except requests.exceptions.ConnectionError as error:
            logging.error(error)

    def _proper_status_code(self, response: requests.Response):
        """Checks if response has proper status code, if not logs an error."""
        if response.status_code in self.error_status_codes:
            logging.error(
                f'Request error for url: {self.url}. Status code: {response.status_code}, Message: {response.text}')
        else:
            return True


class RequestCreator(ABC):

    def __init__(self):
        self.request = Request()
        self.url = None
        self.error_status_codes = None

    @abstractmethod
    def _set_credentials_for_request(self):
        pass

    @abstractmethod
    def get_data(self):
        pass


class AccuWeatherGeopositionRequest(RequestCreator):
    """Geoposition Search for specific latitude and longitude, which needs to be provided via kwargs in get_data method.

    request credentials kwargs:
    apikey = Provided API Key,
    q = Text to search for, should be comma-separated lat/lon pair (lat,lon)."""

    base_url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
    base_url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/seeee'

    def get_data(self, apikey: str, geo_position: str) -> list:
        self._set_credentials_for_request(apikey, geo_position)
        return self.request.get_data()
        # return LOC

    def _set_credentials_for_request(self, apikey: str, geo_position: str):
        self.error_status_codes = [400, 401, 403, 404, 500, 503]
        self.url = self.base_url
        self.request.set_credentials(
            self.url, self.error_status_codes, apikey=apikey, q=geo_position)


class AccuWeather12HoursForecastsRequest(RequestCreator):

    """Forecasts search for specific localization, provided by ID in endpoint.

    request credentials kwargs:
    apikey = Provided API Key"""

    base_url = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour'
    base_url = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12ho'

    def get_data(self, apikey: str, localization_id: str) -> list:
        self._set_credentials_for_request(apikey, localization_id)
        return self.request.get_data()
        # return WEATHER

    def _set_credentials_for_request(self, apikey: str, localization_id: str) -> None:
        self.error_status_codes = [400, 401, 403, 404, 500, 503]
        self.url = self._set_url(localization_id)
        self.request.set_credentials(
            self.url, self.error_status_codes, apikey=apikey)

    def _set_url(self, localization_id: str) -> str:
        return f"{self.base_url}/{localization_id}"
