import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_csv import renderers as r
from weatherapi.apps.weather.rest_api.base.serializers.error_response import (
    ErrorResponseSerializer,
)
from weatherapi.apps.weather.rest_api.base.views.search_weather_forecasts import (
    SearchWeatherForecastsAPIView,
)

LOG = logging.getLogger(__name__)


class ExportWeatherForecastsSearchAPIView(SearchWeatherForecastsAPIView):
    pagination_class = None
    renderer_classes = (r.CSVRenderer,)

    @swagger_auto_schema(
        operation_description="API for searching cached weather forecasts and exporting the result as CSV",
        responses={
            200: openapi.Response(
                "CSV file representing the list of weather forecasts",
                examples={
                    "text/csv": "forecast_span,humidity,lat,lon,misc.clouds,misc.detailed_status,misc.dew_point,misc.feels_like,misc.heat_index,misc.rain,misc.snow,misc.sunrise,misc.sunset,misc.utc_offset,misc.weather_code,misc.weather_icon_name,misc.wind_deg,misc.wind_gust,pressure,temperature,timestamp,timezone,uvi,visibility,weather_desc_main,wind_speed\r\nHour,93.000,30.49,-99.77,90,overcast clouds,8.92,6.74,,0.0,0.0,,,,804,04d,136,,1017.000,10.000,2021-01-23T15:00:00Z,America\/Chicago,0.52,10000.0000,Clouds,4.3200"
                },
            ),
            500: openapi.Response("Error response", schema=ErrorResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        LOG.info(f"Received search weather forecasts request")
        return self.list(request, *args, **kwargs)
