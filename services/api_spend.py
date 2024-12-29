import logging

from models.api_spend import SpendApiRequestData

logger = logging.getLogger(__name__)


def get_spend(function_args: dict) -> dict:
    """
    Get spend data using the function args from the model response.
    """

    try:
        api_request_data = SpendApiRequestData(**function_args)
        logger.info(type(api_request_data))
        return {"data": {"amount": "$25"}}

    except Exception as e:
        logger.error(e)
        return {"error": "An error occurred, please try again later."}
