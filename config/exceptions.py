class GCSClientError(Exception):
    """Raised when there is an error creating the GCS client."""


class GCSFileError(Exception):
    """Raised when there is an issue accessing or processing a GCS file."""


class ResponseExtractionError(Exception):
    """Raised when there is an issue extracting information from the model's response."""
