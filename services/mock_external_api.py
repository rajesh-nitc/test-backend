import logging

from models.mock_external_api import MockExternalApiRequest

logger = logging.getLogger(__name__)


def fetch_mock_data(params: dict = None) -> dict:
    """Mock function to return hardcoded data after validating params."""

    logger.info(f"Received params from Model: {params}")

    try:
        validated_params = MockExternalApiRequest(**params)
        logger.info(f"Validated params: {validated_params}")
        return {"data": {"amount": "$25"}}

    except Exception as e:
        # Catch any kind of exception (validation, network, API, etc.)
        logger.error(f"Error occurred: {e}")
        return {"error": "An error occurred, please try again later."}
