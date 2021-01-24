from rest_framework import serializers


class FetchWeatherForecastsRequestSerializer(serializers.Serializer):
    long = serializers.FloatField(required=True)
    lat = serializers.FloatField(required=True)