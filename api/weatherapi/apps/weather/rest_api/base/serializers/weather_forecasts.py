import json
from enum import Enum

from rest_framework import serializers

from weatherapi.apps.weather.models import ForecastSpan, WeatherForecasts


class WeatherForecastsSerializer(serializers.ModelSerializer):
    forecast_span = serializers.SerializerMethodField()
    misc = serializers.SerializerMethodField()

    class Meta:
        model = WeatherForecasts
        fields = (
            "lon",
            "lat",
            "timestamp",
            "forecast_span",
            "weather_desc_main",
            "timezone",
            "temperature",
            "pressure",
            "humidity",
            "wind_speed",
            "visibility",
            "uvi",
            "misc",
        )

    def get_forecast_span(self, obj: WeatherForecasts):
        if isinstance(obj.forecast_span, Enum):
            # treat forecast_span as Enum and serialize it to its value
            return obj.forecast_span.value
        else:
            return ForecastSpan(obj.forecast_span).value

    def get_misc(self, obj: WeatherForecasts):
        # misc is a dict already, prevent its serialization to string
        return obj.misc
