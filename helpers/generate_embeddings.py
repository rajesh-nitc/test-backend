import pandas as pd
import vertexai
from langchain_text_splitters import RecursiveCharacterTextSplitter
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

from config.settings import settings
from utils.gcs import get_gcs_client

REGION = settings.REGION
GOOGLE_CLOUD_PROJECT = settings.GOOGLE_CLOUD_PROJECT
EMB_MODEL = settings.EMB_MODEL
EMB_BUCKET = settings.EMB_BUCKET
EMB_DIMENSIONALITY = 768
EMB_DF_HEAD = 250
EMB_BLOB = "embeddings.json"
file_path = "data/retail_toy_dataset.csv"


def load_dataset(location) -> pd.DataFrame:
    """Loads the dataset from the specified location"""
    df = pd.read_csv(location)
    df = df.loc[:, ["product_id", "product_name", "description", "list_price"]]
    df = df.dropna()
    return df.head(EMB_DF_HEAD)


def split_product_descriptions(df: pd.DataFrame):
    """Splits long product descriptions into smaller chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        separators=[".", "\n"],
        chunk_size=500,
        chunk_overlap=0,
        length_function=len,
    )
    chunked = []
    for _, row in df.iterrows():
        product_name = row["product_name"]
        desc = row["description"]
        list_price = row["list_price"]
        splits = text_splitter.create_documents([desc])
        for s in splits:
            # Add numeric restricts and other metadata
            chunk = {
                "id": product_name,
                "content": s.page_content,
                "numeric_restricts": [
                    {"namespace": "price", "value_float": list_price}
                ],
            }
            chunked.append(chunk)
    return chunked


def generate_vector_embeddings(df: pd.DataFrame, batch_size=5):
    """Generate vector embeddings for each chunk of text and save to GCS."""
    vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=REGION)
    model = TextEmbeddingModel.from_pretrained(EMB_MODEL)  # type: ignore
    chunked = split_product_descriptions(df)
    print(f"chunked: {chunked}")

    for i in range(0, len(chunked), batch_size):
        texts = [x["content"] for x in chunked[i : i + batch_size]]
        inputs = [TextEmbeddingInput(text, "RETRIEVAL_DOCUMENT") for text in texts]
        embeddings = model.get_embeddings(
            inputs,  # type: ignore
            auto_truncate=False,
            output_dimensionality=EMB_DIMENSIONALITY,
        )
        for x, e in zip(chunked[i : i + batch_size], embeddings):
            x["embedding"] = e.values

    product_embeddings = pd.DataFrame(chunked)

    print(product_embeddings.head(25))

    # Save as JSONL to GCS
    save_to_gcs_as_json(product_embeddings, EMB_BUCKET, EMB_BLOB)  # type: ignore

    return product_embeddings


def save_to_gcs_as_json(dataframe: pd.DataFrame, bkt: str, blob_name: str):
    """
    Save a DataFrame as a JSON in a GCS bucket.
    """
    # Convert DataFrame to JSON string
    json_string = dataframe.to_json(
        orient="records", lines=True
    )  # 'records' for each row as a dict

    # Initialize GCS client
    storage_client = get_gcs_client()
    bucket = storage_client.bucket(bkt)
    blob = bucket.blob(blob_name)

    # Upload JSON string to GCS
    blob.upload_from_string(json_string, content_type="application/json")
    print(f"File saved to GCS: gs://{bucket}/{blob_name}")


def main():
    df = load_dataset(file_path)
    generate_vector_embeddings(df)


if __name__ == "__main__":
    main()
