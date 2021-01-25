from datetime import datetime
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

from pyowm.commons.exceptions import (
    APIRequestError,
    APIResponseError,
    ConfigurationError,
)
from pyowm.weatherapi25.one_call import OneCall
from pyowm.weatherapi25.weather_manager import WeatherManager
from weatherapi.apps.weather.models import ForecastSpan
from weatherapi.apps.weather.tests.weather_data_integrations.open_weather import (
    OpenWeatherGatewayVCRMixin,
)
from weatherapi.apps.weather.tests.weather_data_integrations.open_weather.fixtures import (
    get_sample_one_call_response,
)
from weatherapi.apps.weather.weather_data_integrations.base import (
    WeatherIntegrationGatewayException,
)
from weatherapi.apps.weather.weather_data_integrations.open_weather import (
    OpenWeatherGateway,
)
from weatherapi.settings import env


class OpenWeatherGatewayTestCase(OpenWeatherGatewayVCRMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.open_weather_gateway = OpenWeatherGateway(env("OPEN_WEATHER_MAP_KEY"))
        self.valid_long = 139
        self.valid_lat = 35

    def test_fetch_weather_data_returns_correct_data(self):
        weather_forecasts: OneCall = self.open_weather_gateway._fetch_weather_data(
            self.valid_long, self.valid_lat
        )

        # hourly weather of 2 days
        self.assertEqual(48, weather_forecasts.forecast_hourly.__len__())

        # daily weather of current day + 7 days
        self.assertEqual(8, weather_forecasts.forecast_daily.__len__())

        # current weather
        self.assertIsNotNone(weather_forecasts.current)

    def test_fetch_weather_data_handles_open_weather_exceptions(self):
        with patch.object(WeatherManager, "one_call", side_effect=ConfigurationError()):
            with self.assertRaises(WeatherIntegrationGatewayException):
                self.open_weather_gateway._fetch_weather_data(
                    self.valid_long, self.valid_lat
                )

        with patch.object(WeatherManager, "one_call", side_effect=APIRequestError()):
            with self.assertRaises(WeatherIntegrationGatewayException):
                self.open_weather_gateway._fetch_weather_data(
                    self.valid_long, self.valid_lat
                )

        with patch.object(WeatherManager, "one_call", side_effect=APIResponseError()):
            with self.assertRaises(WeatherIntegrationGatewayException):
                self.open_weather_gateway._fetch_weather_data(
                    self.valid_long, self.valid_lat
                )

    def test_extract_curated_weather_forecasts_curates_hourly_forecast_correctly(self):
        one_call_json_response = get_sample_one_call_response(daily_forecasts=[])
        curated_forecasts = (
            self.open_weather_gateway._extract_curated_weather_forecasts(
                OneCall.from_dict(one_call_json_response)
            )
        )
        # 1 current + 2 hourly
        self.assertEqual(3, curated_forecasts.__len__())

        # temperature conversion(for hourly, temp remains same)
        self.assertEqual(Decimal("278.200"), round(curated_forecasts[2].temp, 3))

        # feels-like conversion(for hourly, feels-like remains same)
        self.assertEqual(Decimal("274.120"), round(curated_forecasts[2].feels_like, 3))

        # rain conversion(for hourly, rain is taken from rain.1h)
        self.assertEqual(Decimal("30.650"), round(curated_forecasts[2].rain, 3))

        # snow conversion(for hourly, snow is taken from snow.1h)
        self.assertEqual(Decimal("30.650"), round(curated_forecasts[1].snow, 3))

        # other general attrs
        self.assertEqual(ForecastSpan.HOUR, curated_forecasts[2].forecast_span)
        self.assertEqual("Asia/Tokyo", curated_forecasts[2].timezone)
        self.assertEqual(86, curated_forecasts[2].humidity)
        self.assertEqual(
            datetime.fromisoformat("2021-01-24 22:00:00"),
            curated_forecasts[2].timestamp,
        )

    def test_extract_curated_weather_forecasts_curates_current_forecast_correctly(self):
        one_call_json_response = get_sample_one_call_response(
            daily_forecasts=[], hourly_forecasts=[]
        )
        curated_forecasts = (
            self.open_weather_gateway._extract_curated_weather_forecasts(
                OneCall.from_dict(one_call_json_response)
            )
        )
        # 1 current
        self.assertEqual(1, curated_forecasts.__len__())

        # temperature conversion(for current, temp remains same)
        self.assertEqual(Decimal("277.59"), round(curated_forecasts[0].temp, 3))

        # feels-like conversion(for current, feels-like remains same)
        self.assertEqual(Decimal("275.46"), round(curated_forecasts[0].feels_like, 3))

        # rain conversion(for current, rain is taken from rain.1h)
        self.assertEqual(Decimal(0), round(curated_forecasts[0].rain, 3))

        # snow conversion(for current, snow is taken from snow.1h)
        self.assertEqual(Decimal(0), round(curated_forecasts[0].snow, 3))

        # other general attrs
        self.assertEqual(ForecastSpan.INSTANT, curated_forecasts[0].forecast_span)
        self.assertEqual("Asia/Tokyo", curated_forecasts[0].timezone)
        self.assertEqual(90, curated_forecasts[0].humidity)
        self.assertEqual(
            datetime.fromisoformat("2021-01-24 21:38:30"),
            curated_forecasts[0].timestamp,
        )

    def test_extract_curated_weather_forecasts_curates_daily_forecast_correctly(self):
        one_call_json_response = get_sample_one_call_response(hourly_forecasts=[])
        curated_forecasts = (
            self.open_weather_gateway._extract_curated_weather_forecasts(
                OneCall.from_dict(one_call_json_response)
            )
        )
        # 1current + 2 daily
        self.assertEqual(3, curated_forecasts.__len__())

        # temperature conversion(for current, temp is the average of morn, day, eve, night)
        self.assertEqual(Decimal("280.04"), round(curated_forecasts[1].temp, 3))

        # feels-like conversion(for current, feels-like is the average of morn, day, eve, night)
        self.assertEqual(Decimal("276.158"), round(curated_forecasts[1].feels_like, 3))

        # rain conversion(for current, rain is available on root level)
        self.assertEqual(Decimal("3.760"), round(curated_forecasts[1].rain, 3))

        # snow conversion(for current, snow is taken from snow.1h)
        self.assertEqual(Decimal(0), round(curated_forecasts[1].snow, 3))

        # other general attrs
        self.assertEqual(ForecastSpan.DAY, curated_forecasts[1].forecast_span)
        self.assertEqual("Asia/Tokyo", curated_forecasts[1].timezone)
        self.assertEqual(69, curated_forecasts[1].humidity)
        self.assertEqual(
            datetime.fromisoformat("2021-01-25 02:00:00"),
            curated_forecasts[1].timestamp,
        )
