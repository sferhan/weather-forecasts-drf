from rest_framework.exceptions import APIException

class WeatherAPIException(APIException):
    def __init__(self, details, error_code, errors = {}):
        super().__init__(code= error_code)
        self.error_details = details
        self.errors = errors

class ServiceUnavailable(WeatherAPIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later. We are fixing things at our end.'
    default_code = 'service_unavailable'


class UnexpectedServerError(WeatherAPIException):
    status_code = 500
    default_detail = "We couldn't complete your request due to an unexpected issue, we are looking into it."
    default_code = 'service_error'


class BadRequestError(WeatherAPIException):
    status_code = 400
    default_detail = "Request is missing required arguments"
    default_code = 'bad_request'
