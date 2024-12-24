import logging

from models.api_spend import SpendApiRequestData

logger = logging.getLogger(__name__)


def get_spend(function_args: dict) -> dict:
    """_summary_

    Args:
        function_args (dict): _description_

    Returns:
        dict: _description_
    """

    try:
        api_request_data = SpendApiRequestData(**function_args)
        logger.info(type(api_request_data))
        return {"data": {"amount": "$25"}}

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": "An error occurred, please try again later."}
