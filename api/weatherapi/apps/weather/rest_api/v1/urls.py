from django.urls import path

from weatherapi.apps.weather.rest_api.v1.views import fetch_weather_data, WeatherForecastsSearchAPIView, \
    WeatherForecastsExportSearchAPIView

urlpatterns = [
    path(
        'fetch-weather-data',
        fetch_weather_data,
        name="fetch-weather-data-ep"
    ),
    path(
        'search-weather-data',
        WeatherForecastsSearchAPIView.as_view(),
        name="weather-forecast-search-ep"
    ),
    path(
        'export-search-weather-data',
        WeatherForecastsExportSearchAPIView.as_view(),
        name="weather-forecast-export-search-ep"
    )
]
