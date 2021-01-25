import logging

from django.db import IntegrityError
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from weatherapi.apps.weather.exceptions import (
    BadRequestError,
    ServiceUnavailable,
    UnexpectedServerError,
)
from weatherapi.apps.weather.rest_api.base.serializers.error_response import (
    ErrorResponseSerializer,
)
from weatherapi.apps.weather.rest_api.base.serializers.fetch_weather_forecasts_request import (
    FetchWeatherForecastsRequestSerializer,
)
from weatherapi.apps.weather.rest_api.base.serializers.weather_forecasts import (
    WeatherForecastsSerializer,
)
from weatherapi.apps.weather.weather_data_integrations.base import (
    WeatherIntegrationGatewayException,
)
from weatherapi.apps.weather.weather_data_integrations.open_weather import (
    OpenWeatherGateway,
)
from weatherapi.settings import env

LOG = logging.getLogger(__name__)


@swagger_auto_schema(
    method="get",
    operation_description="Fetches daily weather forecasts for this day and next seven days, hourly forecast for 48"
    " hours and current weather for location represented by longitude and latitude, caches them "
    "and returns the list of fetched forecasts - Not Paginated",
    query_serializer=FetchWeatherForecastsRequestSerializer,
    responses={
        200: WeatherForecastsSerializer(many=True),
        400: openapi.Response("Bad request", schema=ErrorResponseSerializer),
        500: openapi.Response("Error response", schema=ErrorResponseSerializer),
        503: openapi.Response(
            "Data cannot be fetched from service provider",
            schema=ErrorResponseSerializer,
        ),
    },
)
@api_view(["GET"])
def fetch_weather_data(request: HttpRequest) -> JsonResponse:
    LOG.info(f"Received fetch-weather-data request")
    params = FetchWeatherForecastsRequestSerializer(
        data={
            "long": request.GET.get("long", None),
            "lat": request.GET.get("lat", None),
        }
    )

    if not params.is_valid():
        raise BadRequestError(
            details="", error_code="bad-request", errors=params.errors
        )

    LOG.info(
        f"Precessing fetch-weather-info request with params: {params.validated_data}"
    )

    try:
        LOG.info(f"Initializing Open Weather Gateway")
        weather_gateway = OpenWeatherGateway(env("OPEN_WEATHER_MAP_KEY"))

        LOG.info(f"Fetching weather forecasts from Open Weather Gateway")
        weather_forecasts = weather_gateway.get_weather_by_coords(
            params.validated_data["long"], params.validated_data["lat"]
        )
        LOG.info(f"Successfully fetched weather forecasts")
    except WeatherIntegrationGatewayException as e:
        LOG.exception(f"Exception occurred while fetching weather data. {e}")
        raise ServiceUnavailable(details=str(e), error_code=e.code)

    LOG.info(f"Caching weather forecasts")
    weather_forecasts_model_objs = []
    for forecast in weather_forecasts:
        try:
            model_obj = forecast.to_weather_forecast_record()
            weather_forecasts_model_objs.append(model_obj)
            model_obj.save()
        except IntegrityError as e:
            # occurs due to a failing constraint when duplicate record is tried to be inserted
            # ignoring this should be safe because it means we already have this data in our database
            LOG.warning(
                f"An error occurred while saving weather forecast: {forecast}. Details: {e}"
            )

    LOG.info(f"Serializing weather forecasts")
    try:
        return JsonResponse(
            data=WeatherForecastsSerializer(
                weather_forecasts_model_objs, many=True
            ).data,
            safe=False,
        )
    except Exception as e:
        LOG.info(f"Exception occurred while serializing weather forecasts")
        # failure in serializing the response
        raise UnexpectedServerError(details=str(e), error_code="unknown")
