import logging

import django_filters
from django.http import HttpRequest, JsonResponse
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework_csv import renderers as r

from weatherapi.apps.weather.exceptions import ServiceUnavailable, UnexpectedServerError, BadRequestError
from weatherapi.apps.weather.integrations_gateways import WeatherIntegrationGatewayException
from weatherapi.apps.weather.integrations_gateways.open_weather import OpenWeatherGateway
from weatherapi.apps.weather.models import WeatherForecasts
from weatherapi.apps.weather.rest_api.v1.serializers import WeatherForecastsSerializer, LongLatSerializer
from weatherapi.settings import env

LOG = logging.getLogger(__name__)


@api_view(['GET'])
def fetch_weather_data(request: HttpRequest) -> JsonResponse:
    LOG.info(f"Received fetch-weather-data request")
    params = LongLatSerializer(data={
        'long': request.GET.get('long', None),
        'lat': request.GET.get('lat', None),
    })

    if not params.is_valid():
        raise BadRequestError(details="", error_code='bad-request', errors=params.errors)

    LOG.info(f"Precessing fetch-weather-info request with params: {params.validated_data}")

    try:
        weather_gateway = OpenWeatherGateway(env('OPEN_WEATHER_MAP_KEY'))

        weather_forecasts = weather_gateway.get_weather_by_coords(params.validated_data['long'], params.validated_data['lat'])
    except WeatherIntegrationGatewayException as e:
        LOG.exception(f"Exception occurred while fetching weather data. {e}")
        raise ServiceUnavailable(details=str(e), error_code=e.code)

    weather_forecasts_model_objs = []
    for forecast in weather_forecasts:
        try:
            model_obj = forecast.to_weather_forecast_record()
            weather_forecasts_model_objs.append(model_obj)
            model_obj.save()
        except Exception as e:
            # occurs due to a failing constraint when duplicate record is tried to be inserted
            # ignoring this should be safe because it means we already have this data in our database
            LOG.warning(f"An error occurred while saving weather forecast: {forecast}. Details: {e}")

    try:
        return JsonResponse(data=WeatherForecastsSerializer(weather_forecasts_model_objs, many=True).data, safe=False)
    except Exception as e:
        # failure in serializing the response
        raise UnexpectedServerError(details=str(e), error_code='unknown')


FILTER_MAP = {
    'datetime': ['exact', 'lte', 'gte', 'lt', 'gt'],
    'searchable_string': ['exact', 'iexact', 'contains', 'startswith', 'endswith'],
    'abs': ['exact'],
    'number': ['exact', 'lte', 'gte', 'lt', 'gt']
}

class WeatherForecastsFilter(django_filters.FilterSet):
    class Meta:
        model = WeatherForecasts
        exclude = ['misc']
        fields = {
            'lon': FILTER_MAP['abs'],
            'lat': FILTER_MAP['abs'],
            'timestamp': FILTER_MAP['datetime'],
            'forecast_span': FILTER_MAP['abs'],
            'weather_desc_main': FILTER_MAP['searchable_string'],
            'timezone': FILTER_MAP['searchable_string'],
            'temperature': FILTER_MAP['number'],
            'pressure': FILTER_MAP['number'],
            'humidity': FILTER_MAP['number'],
            'wind_speed': FILTER_MAP['number'],
            'visibility': FILTER_MAP['number'],
            'uvi': FILTER_MAP['number'],
        }

class WeatherForecastsSearchAPIView(ListAPIView):
    """
    API view to retrieve list of weather-forecasts
    """
    serializer_class = WeatherForecastsSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = WeatherForecastsFilter
    queryset = WeatherForecasts.objects.all()
    ordering_fields = ('timestamp', 'temperature', 'pressure')
    ordering = ('timestamp')


class WeatherForecastsExportSearchAPIView(WeatherForecastsSearchAPIView):
    pagination_class = None
    renderer_classes = (r.CSVRenderer, )
