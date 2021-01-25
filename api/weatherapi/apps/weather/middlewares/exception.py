from django.http import JsonResponse
from rest_framework.views import exception_handler

from weatherapi.apps.weather.exceptions import WeatherAPIException
from weatherapi.apps.weather.rest_api.base.serializers.error_response import ErrorResponseSerializer


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    is_weather_api_exc = isinstance(exc, WeatherAPIException)
    if response is not None:
        error_serializer = ErrorResponseSerializer(data={
            'summary': response.data.get('detail', ''),
            'detail': exc.error_details if is_weather_api_exc else '',
            'errors': exc.errors if is_weather_api_exc else {}
        })
        response.data = error_serializer.initial_data
    else:
        error_serializer = ErrorResponseSerializer(data={
            'summary': "We couldn't complete your request due to an unexpected issue, we are looking into it.",
            'detail': str(exc),
            'errors': {}
        })
        response = JsonResponse(data=error_serializer.initial_data, status=500)

    return response