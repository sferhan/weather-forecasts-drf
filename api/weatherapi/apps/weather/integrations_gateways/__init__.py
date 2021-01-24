import abc
import logging
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List

from rest_framework.exceptions import APIException

from weatherapi.apps.weather.models import ForecastSpan, WeatherForecasts

LOG = logging.getLogger(__name__)

class WeatherIntegrationGatewayExceptionCode(Enum):
    UNKNOWN = "Unknown"
    CONFIGURATION = "Configuration"
    REQUEST = "Request"
    RESPONSE = "Response"


class WeatherIntegrationGatewayException(Exception):
    def __init__(self, message: str, base_exception: Exception, code: str):
        super().__init__(message)

        self.code = code
        self.base_exception = base_exception

    def __str__(self):
        return f"Summary: Code-{self.code}, BaseException-{type(self.base_exception)}. Detail: {super().__str__()}"

    @classmethod
    def unexpected_issue(cls, base_exception: Exception):
        return cls('Something went wrong while fetching weather info.', base_exception= base_exception, code=WeatherIntegrationGatewayExceptionCode.UNKNOWN.value)

    def to_api_exception(self):
        return APIException()


@dataclass
class WeatherForecast:
    lon: Decimal
    lat: Decimal
    timezone: str
    timestamp: datetime
    temp: Decimal
    pressure: Decimal
    humidity: int
    clouds: int
    wind_speed: Decimal
    wind_deg: int
    rain: Decimal
    snow: Decimal
    status: str
    detailed_status: str
    weather_code: int
    weather_icon_name: str
    visibility_distance: Decimal
    forecast_span: ForecastSpan
    dew_point: Decimal
    heat_index: Decimal
    utc_offset: int = None
    uvi: Decimal = None
    sunrise: datetime = None
    sunset: datetime = None
    feels_like: Decimal = None
    wind_gust: Decimal = None

    def to_weather_forecast_record(self) -> WeatherForecasts:
        return WeatherForecasts(
            lon = self.lon,
            lat = self.lat,
            timestamp = self.timestamp,
            forecast_span=self.forecast_span.value,
            weather_desc_main=self.status,
            timezone=self.timezone,
            temperature=self.temp,
            pressure=self.pressure,
            humidity=self.humidity,
            wind_speed=self.wind_speed,
            visibility=self.visibility_distance,
            uvi=self.uvi,
            misc={
                'clouds': self.clouds,
                'wind_deg': self.wind_deg,
                'rain': self.rain,
                'snow': self.snow,
                'detailed_status': self.detailed_status,
                'weather_code': self.weather_code,
                'weather_icon_name': self.weather_icon_name,
                'dew_point': self.dew_point,
                'heat_index': self.heat_index,
                'utc_offset': self.utc_offset,
                'sunrise': self.sunrise,
                'sunset': self.sunset,
                'feels_like': self.feels_like,
                'wind_gust': self.wind_gust
            }
        )

    def __str__(self):
        return f"{self.lon}, {self.lat}, {self.timestamp}, {self.forecast_span.value}"


class WeatherIntegrationGateway:
    __metaclass__ = abc.ABCMeta

    def get_weather_by_coords(self, long, lat) -> List[WeatherForecast]:
        try:
            weather_api_resonse = self.fetch_weather_data(long, lat)
            return self.extract_curated_weather_forecasts(weather_api_resonse)
        except Exception as e:
            LOG.info(f"Exception occurred while fetching data from weather integration gateway.", exc_info=True)
            if isinstance(e, WeatherIntegrationGatewayException):
                raise e
            else:
                raise WeatherIntegrationGatewayException.unexpected_issue(e)

    @abc.abstractmethod
    def fetch_weather_data(self, long, lat) -> dict:
        pass

    @abc.abstractmethod
    def extract_curated_weather_forecasts(self, weather_api_response):
        pass
