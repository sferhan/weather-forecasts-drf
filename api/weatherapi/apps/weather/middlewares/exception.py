from django.http import JsonResponse
from rest_framework.views import exception_handler

from weatherapi.apps.weather.exceptions import WeatherAPIException


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    is_weather_api_exc = isinstance(exc, WeatherAPIException)
    if response is not None:
        response.data['summary'] = response.data.get('detail', '')
        response.data['detail'] = exc.error_details if is_weather_api_exc else ''
        response.data['errors'] = exc.errors if is_weather_api_exc else {}
    else:
        data = {}
        data['summary'] = "We couldn't complete your request due to an unexpected issue, we are looking into it."
        data['detail'] = str(exc)
        data['errors'] = {}
        response = JsonResponse(data=data, status=500)

    return response