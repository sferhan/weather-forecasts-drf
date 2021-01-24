import logging
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from weatherapi.apps.weather.models import WeatherForecasts
from weatherapi.apps.weather.rest_api.base.filters.weather_forecasts import WeatherForecastsFilter
from weatherapi.apps.weather.rest_api.base.serializers.weather_forecasts import WeatherForecastsSerializer

LOG = logging.getLogger(__name__)


class SearchWeatherForecastsAPIView(ListAPIView):
    """
    API view to retrieve list of weather-forecasts
    """
    serializer_class = WeatherForecastsSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = WeatherForecastsFilter
    queryset = WeatherForecasts.objects.all()
    ordering_fields = ('timestamp', 'temperature', 'pressure')
    ordering = ('timestamp')