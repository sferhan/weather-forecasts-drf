import logging

from django.db import IntegrityError
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view
from weatherapi.apps.weather.exceptions import ServiceUnavailable, UnexpectedServerError, BadRequestError
from weatherapi.apps.weather.weather_data_integrations.base import WeatherIntegrationGatewayException
from weatherapi.apps.weather.weather_data_integrations.open_weather import OpenWeatherGateway
from weatherapi.apps.weather.rest_api.base.serializers.fetch_weather_forecasts_request import \
    FetchWeatherForecastsRequestSerializer
from weatherapi.apps.weather.rest_api.base.serializers.weather_forecasts import WeatherForecastsSerializer
from weatherapi.settings import env

LOG = logging.getLogger(__name__)


@api_view(['GET'])
def fetch_weather_data(request: HttpRequest) -> JsonResponse:
    LOG.info(f"Received fetch-weather-data request")
    params = FetchWeatherForecastsRequestSerializer(data={
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
        except IntegrityError as e:
            # occurs due to a failing constraint when duplicate record is tried to be inserted
            # ignoring this should be safe because it means we already have this data in our database
            LOG.warning(f"An error occurred while saving weather forecast: {forecast}. Details: {e}")

    try:
        return JsonResponse(data=WeatherForecastsSerializer(weather_forecasts_model_objs, many=True).data, safe=False)
    except Exception as e:
        # failure in serializing the response
        raise UnexpectedServerError(details=str(e), error_code='unknown')