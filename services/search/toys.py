import logging

from models.search.toys import SearchToysApiRequestData
from services.search.vector_search import get_vector_index_data

logger = logging.getLogger(__name__)


async def search_toys(function_args: dict) -> list[dict[str, str]]:
    """
    Search for toys using the function args from the model response.
    """

    try:
        model_instance = SearchToysApiRequestData.model_validate(function_args)
        logger.info(model_instance.model_dump())
        response = get_vector_index_data(function_args=model_instance.model_dump())
        logger.info(response)
        return response

    except Exception as e:
        logger.error(e)
        return [{"error": "An error occurred, please try again later."}]
