import logging

import django_filters
from weatherapi.apps.weather.models import WeatherForecasts
from weatherapi.apps.weather.rest_api.base.filters import FILTER_MAP

LOG = logging.getLogger(__name__)


class WeatherForecastsFilter(django_filters.FilterSet):
    class Meta:
        model = WeatherForecasts
        exclude = ["misc"]
        fields = {
            "lon": FILTER_MAP["abs"],
            "lat": FILTER_MAP["abs"],
            "timestamp": FILTER_MAP["datetime"],
            "forecast_span": FILTER_MAP["abs"],
            "weather_desc_main": FILTER_MAP["searchable_string"],
            "timezone": FILTER_MAP["searchable_string"],
            "temperature": FILTER_MAP["number"],
            "pressure": FILTER_MAP["number"],
            "humidity": FILTER_MAP["number"],
            "wind_speed": FILTER_MAP["number"],
            "visibility": FILTER_MAP["number"],
            "uvi": FILTER_MAP["number"],
        }
