import logging

from models.spend_api import MockExternalApiRequest

logger = logging.getLogger(__name__)


def get_spend(function_args: dict) -> dict:
    """_summary_

    Args:
        function_args (dict): _description_

    Returns:
        dict: _description_
    """

    try:
        validate_function_args = MockExternalApiRequest(**function_args)
        logger.info(f"Validated function_args: {validate_function_args}")
        return {"data": {"amount": "$25"}}

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": "An error occurred, please try again later."}
