import logging

from models.mock_external_api import MockExternalApiRequest

logger = logging.getLogger(__name__)


def fetch_mock_data(params: dict) -> dict:
    """_summary_

    Args:
        params (dict): _description_

    Returns:
        dict: _description_
    """

    logger.info(f"Received params from Model: {params}")

    try:
        validated_params = MockExternalApiRequest(**params)
        logger.info(f"Validated params: {validated_params}")
        return {"data": {"amount": "$25"}}

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": "An error occurred, please try again later."}
