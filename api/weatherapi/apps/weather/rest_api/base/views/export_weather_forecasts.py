import logging
from rest_framework_csv import renderers as r
from weatherapi.apps.weather.rest_api.base.views.search_weather_forecasts import SearchWeatherForecastsAPIView
LOG = logging.getLogger(__name__)


class ExportWeatherForecastsSearchAPIView(SearchWeatherForecastsAPIView):
    pagination_class = None
    renderer_classes = (r.CSVRenderer, )
