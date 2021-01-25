from datetime import datetime
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from weatherapi.apps.weather.models import ForecastSpan, WeatherForecasts
from weatherapi.apps.weather.weather_data_integrations.base import (
    WeatherDataIntegrationGateway,
    WeatherForecast,
    WeatherIntegrationGatewayException,
)
from weatherapi.apps.weather.weather_data_integrations.base.exceptions import (
    WeatherIntegrationGatewayExceptionCode,
)


class FetchWeatherForecastsTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.fetch_weather_forecasts_ep = reverse("v1:fetch-weather-data-ep")

    def _build_fetch_weather_forecasts_params(self, lon, lat):
        params = dict()
        if lon:
            params["long"] = lon
        if lat:
            params["lat"] = lat
        return params

    def _get_weather_forecasts(self):
        return [
            WeatherForecast(
                lon=Decimal(-99.77133),
                lat=Decimal(29.305561),
                timezone="America/Chicago",
                timestamp=datetime.now(),
                temp=Decimal(29.34),
                pressure=Decimal(29.34),
                humidity=49,
                clouds=60,
                wind_speed=Decimal(10.45),
                wind_deg=260,
                rain=Decimal(0),
                snow=Decimal(0),
                status="Cloudy",
                detailed_status="overcast clouds",
                weather_code=804,
                weather_icon_name="04n",
                visibility_distance=None,
                dew_point=Decimal(-8.567),
                heat_index=None,
                utc_offset=None,
                uvi=None,
                sunrise=None,
                sunset=None,
                feels_like=Decimal(29.34),
                wind_gust=None,
                forecast_span=ForecastSpan.HOUR,
            ),
            WeatherForecast(
                lon=Decimal(-99.77133),
                lat=Decimal(29.305561),
                timezone="America/Chicago",
                timestamp=datetime.now(),
                temp=Decimal(29.34),
                pressure=Decimal(29.34),
                humidity=49,
                clouds=60,
                wind_speed=Decimal(10.45),
                wind_deg=260,
                rain=Decimal(0),
                snow=Decimal(0),
                status="Cloudy",
                detailed_status="overcast clouds",
                weather_code=804,
                weather_icon_name="04n",
                visibility_distance=None,
                dew_point=Decimal(-8.567),
                heat_index=None,
                utc_offset=None,
                uvi=None,
                sunrise=None,
                sunset=None,
                feels_like=Decimal(29.34),
                wind_gust=None,
                forecast_span=ForecastSpan.INSTANT,
            ),
            WeatherForecast(
                lon=Decimal(-99.77133),
                lat=Decimal(29.305561),
                timezone="America/Chicago",
                timestamp=datetime.now(),
                temp=Decimal(29.34),
                pressure=Decimal(29.34),
                humidity=49,
                clouds=60,
                wind_speed=Decimal(10.45),
                wind_deg=260,
                rain=Decimal(0),
                snow=Decimal(0),
                status="Cloudy",
                detailed_status="overcast clouds",
                weather_code=804,
                weather_icon_name="04n",
                visibility_distance=None,
                dew_point=Decimal(-8.567),
                heat_index=None,
                utc_offset=None,
                uvi=None,
                sunrise=None,
                sunset=None,
                feels_like=Decimal(29.34),
                wind_gust=None,
                forecast_span=ForecastSpan.DAY,
            ),
        ]

    @patch.object(WeatherDataIntegrationGateway, "get_weather_by_coords")
    def test_fetch_weather_forecasts_correctly_caches_data(self, get_weather_mock):
        get_weather_mock.return_value = self._get_weather_forecasts()
        # initial data
        response1 = self.client.get(
            self.fetch_weather_forecasts_ep,
            self._build_fetch_weather_forecasts_params(-99.77133, 29.305561),
        )
        self.assertEqual(3, WeatherForecasts.objects.all().__len__())

        # verify that the duplicate data is ignored
        response2 = self.client.get(
            self.fetch_weather_forecasts_ep,
            self._build_fetch_weather_forecasts_params(-99.77133, 29.305561),
        )
        self.assertEqual(3, WeatherForecasts.objects.all().__len__())

        self.assertEqual(response1.json().__len__(), response2.json().__len__())

    @patch.object(WeatherDataIntegrationGateway, "get_weather_by_coords")
    def test_fetch_weather_forecasts_returns_data_correctly(self, get_weather_mock):
        get_weather_mock.return_value = self._get_weather_forecasts()

        response = self.client.get(
            self.fetch_weather_forecasts_ep,
            self._build_fetch_weather_forecasts_params(-99.77133, 29.305561),
        )

        get_weather_mock.assert_called_once()

        response_payload = response.json()
        self.assertEqual(3, response_payload.__len__())

    @patch.object(WeatherDataIntegrationGateway, "get_weather_by_coords")
    def test_fetch_weather_forecasts_handles_invalid_params(self, _):
        # no params
        response = self.client.get(
            self.fetch_weather_forecasts_ep,
            self._build_fetch_weather_forecasts_params(None, None),
        )
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(
            {
                "detail": "",
                "summary": "Request is missing required arguments",
                "errors": {
                    "long": ["This field may not be null."],
                    "lat": ["This field may not be null."],
                },
            },
            response.json(),
        )

        # one param
        response = self.client.get(
            self.fetch_weather_forecasts_ep,
            self._build_fetch_weather_forecasts_params(None, 29.305561),
        )
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(
            {
                "detail": "",
                "summary": "Request is missing required arguments",
                "errors": {"long": ["This field may not be null."]},
            },
            response.json(),
        )

        # non decimal param
        response = self.client.get(
            self.fetch_weather_forecasts_ep,
            self._build_fetch_weather_forecasts_params("ancd", None),
        )
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(
            {
                "detail": "",
                "summary": "Request is missing required arguments",
                "errors": {
                    "lat": ["This field may not be null."],
                    "long": ["A valid number is required."],
                },
            },
            response.json(),
        )

    @patch.object(WeatherDataIntegrationGateway, "get_weather_by_coords")
    def test_fetch_weather_forecasts_handles_unexpected_failure(self, _):
        with patch(
            "weatherapi.apps.weather.rest_api.base.views.fetch_weather_forecasts.env",
            side_effect=Exception("some weird issue"),
        ):
            response = self.client.get(
                self.fetch_weather_forecasts_ep,
                self._build_fetch_weather_forecasts_params(-99.77133, 29.305561),
            )
            self.assertEqual(500, response.status_code)
            self.assertEqual(
                "We couldn't complete your request due to an unexpected issue, we are looking into it.",
                response.json()["summary"],
            )
            self.assertEqual("some weird issue", response.json()["detail"])

    @patch.object(WeatherDataIntegrationGateway, "get_weather_by_coords")
    def test_fetch_weather_forecasts_handles_exception_while_fetching_weather_data(
        self, get_weather_mock
    ):
        get_weather_mock.side_effect = WeatherIntegrationGatewayException(
            f"Unable to fetch weather data",
            Exception(),
            WeatherIntegrationGatewayExceptionCode.CONFIGURATION.value,
        )
        response = self.client.get(
            self.fetch_weather_forecasts_ep,
            self._build_fetch_weather_forecasts_params(-99.77133, 29.305561),
        )
        self.assertEqual(503, response.status_code)
        self.assertEqual(
            "Service temporarily unavailable, try again later. We are fixing things at our end.",
            response.json()["summary"],
        )
        self.assertEqual(
            "Summary: Code-Configuration, BaseException-<class 'Exception'>. Detail: Unable to fetch weather data",
            response.json()["detail"],
        )
