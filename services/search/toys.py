import logging

from models.search.toys import SearchToysApiRequestData
from services.search.vector_search import get_vector_index_data

logger = logging.getLogger(__name__)


async def search_toys(function_args: dict) -> list[dict[str, str]]:
    """
    Calls Vertex AI Vector Search index and return list of toys
    """
    try:
        model_instance = SearchToysApiRequestData.model_validate(function_args)
        logger.info(f"Validated function arguments: {model_instance.model_dump()}")

        response = get_vector_index_data(function_args=model_instance.model_dump())
        logger.info(f"Search response: {response}")

        return response

    except Exception as e:
        logger.error(e)
        return [{"error": str(e)}]
