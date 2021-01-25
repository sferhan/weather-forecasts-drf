import logging

from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from django_filters import rest_framework as filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from weatherapi.apps.weather.models import WeatherForecasts
from weatherapi.apps.weather.rest_api.base.filters.weather_forecasts import (
    WeatherForecastsFilter,
)
from weatherapi.apps.weather.rest_api.base.serializers.error_response import (
    ErrorResponseSerializer,
)
from weatherapi.apps.weather.rest_api.base.serializers.weather_forecasts import (
    WeatherForecastsSerializer,
)

LOG = logging.getLogger(__name__)


class SearchWeatherForecastsAPIView(ListAPIView):
    """
    API view to retrieve list of weather-forecasts
    """

    serializer_class = WeatherForecastsSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = WeatherForecastsFilter
    queryset = WeatherForecasts.objects.all()
    ordering_fields = ("timestamp", "temperature", "pressure")
    ordering = "timestamp"

    @swagger_auto_schema(
        operation_description="API for searching cached weather forecasts based on several filters",
        responses={
            500: openapi.Response("Error response", schema=ErrorResponseSerializer)
        },
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
