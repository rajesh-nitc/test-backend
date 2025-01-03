from logging.config import dictConfig
from typing import Any

LOGGING_CONFIG: Any = {
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
            "level": "NOTSET",  # Handler will respect logger's level
        },
    },
    "root": {  # Root logger configuration
        "handlers": ["console"],
        "level": "INFO",
    },
}


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure logging for the application.
    :param log_level: The global log level for the root logger.
    """
    # Update the root logger level dynamically
    LOGGING_CONFIG["root"]["level"] = log_level.upper()
    dictConfig(LOGGING_CONFIG)
