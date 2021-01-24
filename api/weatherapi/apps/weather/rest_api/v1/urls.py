from django.urls import path

from weatherapi.apps.weather.rest_api.base.views.export_weather_forecasts import ExportWeatherForecastsSearchAPIView
from weatherapi.apps.weather.rest_api.base.views.fetch_weather_forecasts import fetch_weather_data
from weatherapi.apps.weather.rest_api.base.views.search_weather_forecasts import SearchWeatherForecastsAPIView

app_name = 'v1'

urlpatterns = [
    path(
        'fetch-weather-forecasts',
        fetch_weather_data,
        name="fetch-weather-data-ep"
    ),
    path(
        'search-weather-forecasts',
        SearchWeatherForecastsAPIView.as_view(),
        name="weather-forecast-search-ep"
    ),
    path(
        'export-search-weather-forecasts',
        ExportWeatherForecastsSearchAPIView.as_view(),
        name="weather-forecast-export-search-ep"
    )
]
