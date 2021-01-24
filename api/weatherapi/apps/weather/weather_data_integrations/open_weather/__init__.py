import logging
from datetime import datetime
from decimal import Decimal
from statistics import mean
from typing import List
from pyowm.commons.enums import SubscriptionTypeEnum
from pyowm.commons.exceptions import ConfigurationError, APIRequestError, APIResponseError
from pyowm.weatherapi25.one_call import OneCall
from pyowm.weatherapi25.weather import Weather
from pyowm.owm import OWM
from weatherapi.apps.weather.models import ForecastSpan
from weatherapi.apps.weather.weather_data_integrations.base import WeatherDataIntegrationGateway, WeatherForecast, \
    WeatherIntegrationGatewayException
from weatherapi.apps.weather.weather_data_integrations.base.exceptions import WeatherIntegrationGatewayExceptionCode

LOG = logging.getLogger(__name__)


class OpenWeatherGateway(WeatherDataIntegrationGateway):
    def __init__(self, open_weather_api_key):
        self._API_KEY = open_weather_api_key
        self.config = {
            'subscription_type': SubscriptionTypeEnum.FREE,
            'language': 'en',
            'connection': {
                'use_ssl': True,
                'verify_ssl_certs': True,
                'use_proxy': False,
                'timeout_secs': 12
            },
            'proxies': {
                'http': 'http://user:pass@host:port',
                'https': 'socks5://user:pass@host:port'
            }
        }
        self.open_weather_client = OWM(self._API_KEY, config=self.config).weather_manager()
        super().__init__()

    def __open_api_weather_to_weather_forcast(self, owm_weather: Weather, forecast_span: ForecastSpan, timezone: str, long, lat):
        if forecast_span is ForecastSpan.DAY:
            temp = Decimal(mean(
                [
                    owm_weather.temp['morn'],
                    owm_weather.temp['day'],
                    owm_weather.temp['eve'],
                    owm_weather.temp['night']
                ]
            ))
            feels_like = Decimal(mean(
                [
                    owm_weather.temp['feels_like_morn'],
                    owm_weather.temp['feels_like_day'],
                    owm_weather.temp['feels_like_eve'],
                    owm_weather.temp['feels_like_night']
                ]
            ))
            rain = Decimal(owm_weather.rain.get('all', 0))
            snow = Decimal(owm_weather.snow.get('all', 0))
        else:
            temp = Decimal(owm_weather.temp['temp'])
            feels_like = Decimal(owm_weather.temp['feels_like'])
            rain = Decimal(owm_weather.rain.get('1h', 0))
            snow = Decimal(owm_weather.snow.get('1h', 0))

        return WeatherForecast(
            lon=long,
            lat=lat,
            timezone = timezone,
            timestamp = datetime.fromtimestamp(owm_weather.ref_time),
            temp = temp,
            pressure = Decimal(owm_weather.pressure['press']),
            humidity = owm_weather.humidity,
            clouds = owm_weather.clouds,
            wind_speed = Decimal(owm_weather.wnd['speed']),
            wind_deg = owm_weather.wnd['deg'],
            rain = rain,
            snow=snow,
            status = owm_weather.status,
            detailed_status = owm_weather.detailed_status,
            weather_code = owm_weather.weather_code,
            weather_icon_name = owm_weather.weather_icon_name,
            visibility_distance = Decimal(owm_weather.visibility_distance) if owm_weather.visibility_distance else None,
            dew_point = Decimal(owm_weather.dewpoint),
            heat_index = Decimal(owm_weather.heat_index) if owm_weather.heat_index else None,
            utc_offset = owm_weather.utc_offset,
            uvi = Decimal(owm_weather.uvi) if owm_weather.uvi else None,
            sunrise = datetime.fromtimestamp(owm_weather.srise_time) if owm_weather.srise_time else None,
            sunset = datetime.fromtimestamp(owm_weather.sset_time) if owm_weather.sset_time else None,
            feels_like = feels_like,
            wind_gust = Decimal(owm_weather.wnd['gust']) if 'gust' in owm_weather.wnd else None,
            forecast_span=forecast_span
        )

    def _fetch_weather_data(self, long, lat) -> dict:
        LOG.info("Fetching weather data from Open Weather Map using 'One Call' API")
        try:
            return self.open_weather_client.one_call(lat=lat, lon=long, exclude='minutely,alerts', units='metric')
        except ConfigurationError as e:
            LOG.info("ConfigurationError occurred while fetching weather data from Open Weather Map")
            raise WeatherIntegrationGatewayException(f"{e}", e, WeatherIntegrationGatewayExceptionCode.CONFIGURATION.value)
        except APIRequestError as e:
            LOG.info("APIRequestError occurred while fetching weather data from Open Weather Map")
            raise WeatherIntegrationGatewayException(f"{e}", e, WeatherIntegrationGatewayExceptionCode.REQUEST.value)
        except APIResponseError as e:
            LOG.info("APIResponseError occurred while fetching weather data from Open Weather Map")
            raise WeatherIntegrationGatewayException(f"{e}", e, WeatherIntegrationGatewayExceptionCode.RESPONSE.value)

    def _extract_curated_weather_forecasts(self, weather_api_response: OneCall):
        LOG.info("Parsing Open Weather Map 'One Call' API response")
        # add the current forecast as hourly forecast
        weather_forecasts: List[WeatherForecast] = [
            self.__open_api_weather_to_weather_forcast(weather_api_response.current, ForecastSpan.INSTANT, weather_api_response.timezone, weather_api_response.lon, weather_api_response.lat)
        ]

        # add the hourly forecasts
        for forecast in weather_api_response.forecast_hourly:
            weather_forecasts.append(self.__open_api_weather_to_weather_forcast(forecast, ForecastSpan.HOUR, weather_api_response.timezone, weather_api_response.lon, weather_api_response.lat))

        # add daily forecasts
        for forecast in weather_api_response.forecast_daily:
            weather_forecasts.append(self.__open_api_weather_to_weather_forcast(forecast, ForecastSpan.DAY, weather_api_response.timezone, weather_api_response.lon, weather_api_response.lat))

        return weather_forecasts
