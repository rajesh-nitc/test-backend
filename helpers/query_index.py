from dotenv import load_dotenv

load_dotenv()
import logging
import os

import vertexai
from google.cloud import aiplatform_v1
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

logger = logging.getLogger(__name__)

texts = ["what are some outdoor toys for 10 year old kid"]

REGION = os.getenv("REGION")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
MODEL_EMB = os.getenv("MODEL_EMB")

# Set variables for the current deployed index.
API_ENDPOINT = os.getenv("API_ENDPOINT")
INDEX_ENDPOINT = os.getenv("INDEX_ENDPOINT")
DEPLOYED_INDEX_ID = os.getenv("DEPLOYED_INDEX_ID")
DIMENSIONALITY = os.getenv("DIMENSIONALITY")

vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=REGION)
task = "RETRIEVAL_DOCUMENT"
model = TextEmbeddingModel.from_pretrained(MODEL_EMB)  # type: ignore

inputs = [TextEmbeddingInput(text, task) for text in texts]
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
    neighbor_count=3,
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
logger.info(response)


# nearest_neighbors {
#   neighbors {
#     datapoint {
#       datapoint_id: "c73ea622b3be6a3ffa3b0b5490e4929e"
#       crowding_tag {
#         crowding_attribute: "0"
#       }
#     }
#     distance: 0.29053670167922974
#   }
#   neighbors {
#     datapoint {
#       datapoint_id: "dec7bd1f983887650715c6fafaa5b593"
#       crowding_tag {
#         crowding_attribute: "0"
#       }
#     }
#     distance: 0.27769008278846741
#   }
#   neighbors {
#     datapoint {
#       datapoint_id: "7de8b315b3cb91f3680eb5b88a20dcee"
#       crowding_tag {
#         crowding_attribute: "0"
#       }
#     }
#     distance: 0.27526360750198364
#   }
# }
