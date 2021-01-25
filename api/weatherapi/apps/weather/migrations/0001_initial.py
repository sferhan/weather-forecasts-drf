# Generated by Django 2.2.4 on 2021-01-23 02:14

import uuid

import django.utils.timezone
from django.db import migrations, models

import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WeatherForecasts",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("lon", models.DecimalField(decimal_places=2, max_digits=5)),
                ("lat", models.DecimalField(decimal_places=2, max_digits=5)),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "forecast_span",
                    models.CharField(
                        choices=[
                            ("INSTANT", "Instant"),
                            ("HOUR", "Hour"),
                            ("DAY", "Day"),
                        ],
                        max_length=20,
                    ),
                ),
                ("weather_desc_main", models.CharField(max_length=20, null=True)),
                ("timezone", models.CharField(max_length=100, null=True)),
                (
                    "temperature",
                    models.DecimalField(decimal_places=3, max_digits=7, null=True),
                ),
                (
                    "pressure",
                    models.DecimalField(decimal_places=3, max_digits=10, null=True),
                ),
                (
                    "humidity",
                    models.DecimalField(decimal_places=3, max_digits=6, null=True),
                ),
                (
                    "wind_speed",
                    models.DecimalField(decimal_places=4, max_digits=10, null=True),
                ),
                (
                    "visibility",
                    models.DecimalField(decimal_places=4, max_digits=10, null=True),
                ),
                ("uvi", models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ("misc", jsonfield.fields.JSONField(default={})),
            ],
            options={"unique_together": {("lon", "lat", "timestamp", "forecast_span")}},
        )
    ]
