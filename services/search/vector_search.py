import logging

from google.cloud import aiplatform
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import (
    NumericNamespace,
)
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

from config.settings import settings

EMB_MODEL = settings.EMB_MODEL
EMB_INDEX_ENDPOINT = settings.EMB_INDEX_ENDPOINT
EMB_DEPLOYED_INDEX_ID = settings.EMB_DEPLOYED_INDEX_ID
EMB_DIMENSIONALITY = settings.EMB_DIMENSIONALITY

logger = logging.getLogger(__name__)


def get_vector_index_data(function_args: dict) -> list[dict[str, str]]:
    """
    Get search data using the query and numeric filter.
    """
    query = function_args.get("query")
    if not query:
        raise ValueError("Missing required parameter: 'query'")

    top_k = function_args.get("top_k", settings.EMB_TOP_K)
    op = function_args.get("operator")
    price = function_args.get("price")

    # Create numeric_filter only if op and price are provided
    numeric_filter = []
    if op and price is not None:
        price = float(price)  # Explicitly convert price to float
        numeric_filter = [
            NumericNamespace(
                name="price",  # Set the field name to "price"
                value_float=price,  # Set the filter value
                op=op.upper(),  # Ensure the operator is uppercase
            )
        ]

    # query
    query_list = [query]

    model = TextEmbeddingModel.from_pretrained(EMB_MODEL)  # type: ignore
    inputs = [TextEmbeddingInput(text, "RETRIEVAL_DOCUMENT") for text in query_list]  # type: ignore
    kwargs = (
        dict(output_dimensionality=EMB_DIMENSIONALITY) if EMB_DIMENSIONALITY else {}
    )
    embeddings = model.get_embeddings(inputs, **kwargs)  # type: ignore
    feature_vector = [embedding.values for embedding in embeddings]

    index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=EMB_INDEX_ENDPOINT
    )  # type: ignore

    try:
        response = index_endpoint.find_neighbors(
            deployed_index_id=EMB_DEPLOYED_INDEX_ID,  # type: ignore
            queries=[feature_vector[0]],
            num_neighbors=top_k,  # type: ignore
            numeric_filter=numeric_filter,  # type: ignore
        )
    except Exception as e:
        raise RuntimeError(f"Error querying vector index: {e}")

    # Process response (since the response is a list of MatchNeighbor objects, not a dictionary)
    matched_neighbors = response[
        0
    ]  # Extract the list of neighbors (the response is a list)

    # Extract the required data from the neighbors
    results = [
        {
            "id": neighbor.id,
        }
        for neighbor in matched_neighbors
    ]

    return results
