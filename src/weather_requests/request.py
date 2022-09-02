import logging
from abc import ABC, abstractmethod

import requests
from requests.adapters import HTTPAdapter


class Request:

    def __init__(self):
        self.url: str = None
        self.request_params = None
        self.error_status_codes: list = None

    def set_credentials(self, url, error_status_codes: list, **kwargs):
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
        if response.status_code in self.error_status_codes:
            logging.error(
                f'Request error for url: {self.url}. Status code: {response.status_code}, Message: {response.text}')
        else:
            return "True"


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

    def get_data(self, apikey: str, geo_position: str) -> list:
        self._set_credentials_for_request(apikey, geo_position)
        # return self.request.get_data()
        return LOC

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

    def get_data(self, apikey: str, localization_id: str) -> list:
        self._set_credentials_for_request(apikey, localization_id)
        # return self.request.get_data()
        return WEATHER
        
    def _set_credentials_for_request(self, apikey: str, localization_id: str) -> None:
        self.error_status_codes = [400, 401, 403, 404, 500, 503]
        self.url = self._set_url(localization_id)
        self.request.set_credentials(
            self.url, self.error_status_codes, apikey=apikey)

    def _set_url(self, localization_id: str) -> str:
        return f"{self.base_url}/{localization_id}"

WEATHER = [
  {
    "DateTime": "2022-09-02T10:00:00+00:00",
    "EpochDateTime": 1662112800,
    "WeatherIcon": 7,
    "IconPhrase": "Cloudy",
    "HasPrecipitation": "false",
    "IsDaylight": "true",
    "Temperature": {
      "Value": 50,
      "Unit": "F",
      "UnitType": 18
    },
    "PrecipitationProbability": 1,
    "MobileLink": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=10&lang=en-us",
    "Link": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=10&lang=en-us"
  },
  {
    "DateTime": "2022-09-02T11:00:00+00:00",
    "EpochDateTime": 1662116400,
    "WeatherIcon": 6,
    "IconPhrase": "Mostly cloudy",
    "HasPrecipitation": "false",
    "IsDaylight": "true",
    "Temperature": {
      "Value": 51,
      "Unit": "F",
      "UnitType": 18
    },
    "PrecipitationProbability": 1,
    "MobileLink": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=11&lang=en-us",
    "Link": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=11&lang=en-us"
  },
  {
    "DateTime": "2022-09-02T12:00:00+00:00",
    "EpochDateTime": 1662120000,
    "WeatherIcon": 6,
    "IconPhrase": "Mostly cloudy",
    "HasPrecipitation": "false",
    "IsDaylight": "true",
    "Temperature": {
      "Value": 52,
      "Unit": "F",
      "UnitType": 18
    },
    "PrecipitationProbability": 1,
    "MobileLink": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=12&lang=en-us",
    "Link": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=12&lang=en-us"
  },
  {
    "DateTime": "2022-09-02T13:00:00+00:00",
    "EpochDateTime": 1662123600,
    "WeatherIcon": 4,
    "IconPhrase": "Intermittent clouds",
    "HasPrecipitation": "false",
    "IsDaylight": "true",
    "Temperature": {
      "Value": 53,
      "Unit": "F",
      "UnitType": 18
    },
    "PrecipitationProbability": 0,
    "MobileLink": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=13&lang=en-us",
    "Link": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=13&lang=en-us"
  },
  {
    "DateTime": "2022-09-02T14:00:00+00:00",
    "EpochDateTime": 1662127200,
    "WeatherIcon": 2,
    "IconPhrase": "Mostly sunny",
    "HasPrecipitation": "false",
    "IsDaylight": "true",
    "Temperature": {
      "Value": 54,
      "Unit": "F",
      "UnitType": 18
    },
    "PrecipitationProbability": 0,
    "MobileLink": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=14&lang=en-us",
    "Link": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=14&lang=en-us"
  },
  {
    "DateTime": "2022-09-02T15:00:00+00:00",
    "EpochDateTime": 1662130800,
    "WeatherIcon": 1,
    "IconPhrase": "Sunny",
    "HasPrecipitation": "false",
    "IsDaylight": "true",
    "Temperature": {
      "Value": 55,
      "Unit": "F",
      "UnitType": 18
    },
    "PrecipitationProbability": 0,
    "MobileLink": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=15&lang=en-us",
    "Link": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=15&lang=en-us"
  },
  {
    "DateTime": "2022-09-02T16:00:00+00:00",
    "EpochDateTime": 1662134400,
    "WeatherIcon": 2,
    "IconPhrase": "Mostly sunny",
    "HasPrecipitation": "false",
    "IsDaylight": "true",
    "Temperature": {
      "Value": 56,
      "Unit": "F",
      "UnitType": 18
    },
    "PrecipitationProbability": 0,
    "MobileLink": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=16&lang=en-us",
    "Link": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=16&lang=en-us"
  },
  {
    "DateTime": "2022-09-02T17:00:00+00:00",
    "EpochDateTime": 1662138000,
    "WeatherIcon": 3,
    "IconPhrase": "Partly sunny",
    "HasPrecipitation": "false",
    "IsDaylight": "true",
    "Temperature": {
      "Value": 56,
      "Unit": "F",
      "UnitType": 18
    },
    "PrecipitationProbability": 0,
    "MobileLink": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=17&lang=en-us",
    "Link": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=17&lang=en-us"
  },
  {
    "DateTime": "2022-09-02T18:00:00+00:00",
    "EpochDateTime": 1662141600,
    "WeatherIcon": 4,
    "IconPhrase": "Intermittent clouds",
    "HasPrecipitation": "false",
    "IsDaylight": "true",
    "Temperature": {
      "Value": 56,
      "Unit": "F",
      "UnitType": 18
    },
    "PrecipitationProbability": 0,
    "MobileLink": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=18&lang=en-us",
    "Link": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=18&lang=en-us"
  },
  {
    "DateTime": "2022-09-02T19:00:00+00:00",
    "EpochDateTime": 1662145200,
    "WeatherIcon": 3,
    "IconPhrase": "Partly sunny",
    "HasPrecipitation": "false",
    "IsDaylight": "true",
    "Temperature": {
      "Value": 55,
      "Unit": "F",
      "UnitType": 18
    },
    "PrecipitationProbability": 0,
    "MobileLink": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=19&lang=en-us",
    "Link": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=19&lang=en-us"
  },
  {
    "DateTime": "2022-09-02T20:00:00+00:00",
    "EpochDateTime": 1662148800,
    "WeatherIcon": 2,
    "IconPhrase": "Mostly sunny",
    "HasPrecipitation": "false",
    "IsDaylight": "true",
    "Temperature": {
      "Value": 54,
      "Unit": "F",
      "UnitType": 18
    },
    "PrecipitationProbability": 0,
    "MobileLink": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=20&lang=en-us",
    "Link": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=20&lang=en-us"
  },
  {
    "DateTime": "2022-09-02T21:00:00+00:00",
    "EpochDateTime": 1662152400,
    "WeatherIcon": 33,
    "IconPhrase": "Clear",
    "HasPrecipitation": "false",
    "IsDaylight": "false",
    "Temperature": {
      "Value": 53,
      "Unit": "F",
      "UnitType": 18
    },
    "PrecipitationProbability": 0,
    "MobileLink": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=21&lang=en-us",
    "Link": "http://www.accuweather.com/en/is/reykjavik/190390/hourly-weather-forecast/190390?day=1&hbhhour=21&lang=en-us"
  }
]

LOC = {
  "Version": 1,
  "Key": "190390",
  "Type": "City",
  "Rank": 40,
  "LocalizedName": "Reykjavik",
  "EnglishName": "Reykjavik",
  "PrimaryPostalCode": "",
  "Region": {
    "ID": "ARC",
    "LocalizedName": "Arctic",
    "EnglishName": "Arctic"
  },
  "Country": {
    "ID": "IS",
    "LocalizedName": "Iceland",
    "EnglishName": "Iceland"
  },
  "AdministrativeArea": {
    "ID": "1",
    "LocalizedName": "Greater Reykjavik",
    "EnglishName": "Greater Reykjavik",
    "Level": 1,
    "LocalizedType": "Region",
    "EnglishType": "Region",
    "CountryID": "IS"
  },
  "TimeZone": {
    "Code": "GMT",
    "Name": "Atlantic/Reykjavik",
    "GmtOffset": 0,
    "IsDaylightSaving": "false",
    "NextOffsetChange": "null"
  },
  "GeoPosition": {
    "Latitude": 64.137,
    "Longitude": -21.902,
    "Elevation": {
      "Metric": {
        "Value": 36,
        "Unit": "m",
        "UnitType": 5
      },
      "Imperial": {
        "Value": 118,
        "Unit": "ft",
        "UnitType": 0
      }
    }
  },
  "IsAlias": "false",
  "SupplementalAdminAreas": [],
  "DataSets": [
    "AirQualityCurrentConditions",
    "AirQualityForecasts",
    "Alerts",
    "DailyPollenForecast",
    "FutureRadar",
    "MinuteCast",
    "Radar"
  ]
}
