from enum import Enum
from uuid import uuid4

from django.db.models import Model
from django.db import models
from django.utils import timezone
from jsonfield import JSONField


class ForecastSpan(Enum):
    INSTANT = 'Instant'
    HOUR = 'Hour'
    DAY = 'Day'

    @classmethod
    def choices(cls):
        return [(i.name, i.value) for i in cls]


class WeatherForecasts(Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    lon = models.DecimalField(null=False, max_digits=5, decimal_places=2)
    lat = models.DecimalField(null=False, max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(null=False, default=timezone.now)
    forecast_span = models.CharField(null=False, max_length=20, choices=ForecastSpan.choices())
    weather_desc_main = models.CharField(null=True, max_length=20)
    timezone = models.CharField(null=True, max_length=100)
    temperature = models.DecimalField(null=True, max_digits=7, decimal_places=3)
    pressure = models.DecimalField(null=True, max_digits=10, decimal_places=3)
    humidity = models.DecimalField(null=True, max_digits=6, decimal_places=3)
    wind_speed = models.DecimalField(null=True, max_digits=10, decimal_places=4)
    visibility = models.DecimalField(null=True, max_digits=10, decimal_places=4)
    uvi = models.DecimalField(null=True, max_digits=4, decimal_places=2)
    misc = JSONField(null=False, default={})

    class Meta:
        unique_together = (('lon', 'lat', 'timestamp', 'forecast_span'),)


