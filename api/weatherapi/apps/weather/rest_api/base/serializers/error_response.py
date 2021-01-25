from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    summary = serializers.CharField(required=True)
    detail = serializers.CharField(required=True)
    errors = serializers.JSONField(required=True)
