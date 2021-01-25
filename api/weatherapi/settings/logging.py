import logging.config

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "fmt1": {
            "format": "[FMT1] %(asctime)-15s %(message)s",
        },
        "fmt2": {
            "format": "[FMT2] %(asctime)-15s %(message)s",
        },
    },
    "handlers": {
        "console1": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "fmt1",
        },
        "console2": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "fmt2",
        },
    },
    # First config for root logger: console1 -> fmt1
    "root": {
        "handlers": ["console1"],
        "level": "DEBUG",
        "propagate": True,
    },
    "loggers": {
        # Second config for root logger: console2 -> fmt2
        "": {
            "handlers": ["console2"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

logging.config.dictConfig(LOGGING)
