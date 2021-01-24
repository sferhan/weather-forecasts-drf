from django.urls import path, include

from weatherapi.apps.weather.rest_api.v1.urls import urlpatterns as v1_urls

urlpatterns = [
    path(
        'v1/',
        include(v1_urls)
    )
]
