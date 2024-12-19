from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        },
        "detailed": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "INFO",  # Default level, will be updated later
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",  # Default level, will be updated later
            "propagate": False,
        },
    },
}


def setup_logging(log_level="INFO"):
    LOGGING_CONFIG["handlers"]["console"]["level"] = log_level
    LOGGING_CONFIG["loggers"][""]["level"] = log_level
    dictConfig(LOGGING_CONFIG)
