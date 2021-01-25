from django.urls import include, path

from weatherapi.apps.weather.rest_api.v1.urls import urlpatterns as v1_urls

app_name = "v1"

urlpatterns = [path("v1/", include(v1_urls))]
