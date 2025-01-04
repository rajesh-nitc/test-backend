import logging

from models.api.spend import SpendApiRequestData

logger = logging.getLogger(__name__)


async def get_spend(function_args: dict) -> dict:
    """
    Get spend data from the API. This function is a placeholder for the actual API call.
    """

    try:
        model_instance = SpendApiRequestData.model_validate(function_args)
        logger.info(f"Validated function arguments: {model_instance.model_dump()}")
        return {"data": {"amount": "$25"}}

    except Exception as e:
        logger.error(e)
        return {"error": str(e)}
