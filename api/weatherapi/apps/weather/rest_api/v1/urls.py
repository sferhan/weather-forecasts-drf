from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from weatherapi.apps.weather.rest_api.base.views.export_weather_forecasts import ExportWeatherForecastsSearchAPIView
from weatherapi.apps.weather.rest_api.base.views.fetch_weather_forecasts import fetch_weather_data
from weatherapi.apps.weather.rest_api.base.views.search_weather_forecasts import SearchWeatherForecastsAPIView

app_name = 'v1'

schema_view = get_schema_view(
   openapi.Info(
      title="Weather Forecasts API",
      default_version='v1',
      description="API for pulling, caching, searching and exporting weather forecast information",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

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
    ),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
