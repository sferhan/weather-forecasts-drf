import abc
import logging
from typing import List

from weatherapi.apps.weather.weather_data_integrations.base.data_models import WeatherForecast
from weatherapi.apps.weather.weather_data_integrations.base.exceptions import WeatherIntegrationGatewayException

LOG = logging.getLogger(__name__)


class WeatherDataIntegrationGateway:
    __metaclass__ = abc.ABCMeta

    def get_weather_by_coords(self, long, lat) -> List[WeatherForecast]:
        try:
            weather_api_resonse = self._fetch_weather_data(long, lat)
            return self._extract_curated_weather_forecasts(weather_api_resonse)
        except Exception as e:
            LOG.info(f"Exception occurred while fetching data from weather integration gateway.", exc_info=True)
            if isinstance(e, WeatherIntegrationGatewayException):
                raise e
            else:
                raise WeatherIntegrationGatewayException.unexpected_issue(e)

    @abc.abstractmethod
    def _fetch_weather_data(self, long, lat) -> dict:
        pass

    @abc.abstractmethod
    def _extract_curated_weather_forecasts(self, weather_api_response):
        pass
