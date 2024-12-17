import logging

from dotenv import load_dotenv

load_dotenv()
import os

from google.cloud import aiplatform_v1
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

from utils.vertex_ai_vector_index import get_datapoint_ids

MODEL_EMB = os.getenv("MODEL_EMB")
API_ENDPOINT = os.getenv("API_ENDPOINT")
INDEX_ENDPOINT = os.getenv("INDEX_ENDPOINT")
DEPLOYED_INDEX_ID = os.getenv("DEPLOYED_INDEX_ID")
DIMENSIONALITY = int(os.getenv("DIMENSIONALITY"))  # type: ignore
TASK = os.getenv("TASK")

logger = logging.getLogger(__name__)


def get_vector_index_data(function_args: dict):
    query = function_args.get("query")
    if not query:
        raise ValueError("Missing required parameter: 'query'")

    # Extract top_k with a default value of 5
    top_k = function_args.get("top_k", 5)

    query_list = [query]
    model = TextEmbeddingModel.from_pretrained(MODEL_EMB)  # type: ignore
    inputs = [TextEmbeddingInput(text, TASK) for text in query_list]  # type: ignore
    kwargs = dict(output_dimensionality=DIMENSIONALITY) if DIMENSIONALITY else {}
    embeddings = model.get_embeddings(inputs, **kwargs)  # type: ignore
    feature_vector = [embedding.values for embedding in embeddings]

    # Configure Vector Search client
    client_options = {"api_endpoint": API_ENDPOINT}
    vector_search_client = aiplatform_v1.MatchServiceClient(
        client_options=client_options,
    )

    # Build FindNeighborsRequest object
    datapoint = aiplatform_v1.IndexDatapoint(feature_vector=feature_vector[0])

    query = aiplatform_v1.FindNeighborsRequest.Query(
        datapoint=datapoint,
        # The number of nearest neighbors to be retrieved
        neighbor_count=top_k,
    )
    request = aiplatform_v1.FindNeighborsRequest(
        index_endpoint=INDEX_ENDPOINT,
        deployed_index_id=DEPLOYED_INDEX_ID,
        # Request can have multiple queries
        queries=[query],
        return_full_datapoint=False,
    )

    # Execute the request
    response = vector_search_client.find_neighbors(request)

    # Handle the response
    return get_datapoint_ids(response, top_k)
