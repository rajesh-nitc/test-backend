import logging

from services.vertex_ai_vector_search import get_vector_index_data

logger = logging.getLogger(__name__)


def search_toys(function_args: dict):
    """
    Search for toys using the function args from the model response.
    """

    try:
        ids = get_vector_index_data(function_args=function_args)
        logger.info(f"ids: {ids}")
        return ids

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": "An error occurred, please try again later."}
