import logging

from services.vertex_ai_vector_index import get_vector_index_data

logger = logging.getLogger(__name__)


def get_toys(function_args: dict):

    try:
        datapoint_ids = get_vector_index_data(function_args=function_args)
        logger.info(f"datapoint_ids: {datapoint_ids}")
        return datapoint_ids

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": "An error occurred, please try again later."}
