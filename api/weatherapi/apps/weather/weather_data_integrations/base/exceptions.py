import logging
from enum import Enum

from rest_framework.exceptions import APIException

LOG = logging.getLogger(__name__)


class WeatherIntegrationGatewayExceptionCode(Enum):
    UNKNOWN = "Unknown"
    CONFIGURATION = "Configuration"
    REQUEST = "Request"
    RESPONSE = "Response"


class WeatherIntegrationGatewayException(Exception):
    def __init__(self, message: str, base_exception: Exception, code: str):
        super().__init__(message)

        self.code = code
        self.base_exception = base_exception

    def __str__(self):
        return f"Summary: Code-{self.code}, BaseException-{type(self.base_exception)}. Detail: {super().__str__()}"

    @classmethod
    def unexpected_issue(cls, base_exception: Exception):
        return cls(
            "Something went wrong while fetching weather info.",
            base_exception=base_exception,
            code=WeatherIntegrationGatewayExceptionCode.UNKNOWN.value,
        )

    def to_api_exception(self):
        return APIException()
