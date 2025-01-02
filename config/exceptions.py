class QuotaExceededError(Exception):
    """Custom exception raised when the user's quota is exceeded."""


class PromptExceededError(Exception):
    """Custom exception raised when the user's prompt is exceeded."""


class GCSClientError(Exception):
    """Raised when there is an error creating the GCS client."""


class GCSFileError(Exception):
    """Raised when there is an issue accessing or processing a GCS file."""


class QuotaUpdateError(Exception):
    """Raised when there is an issue updating quota usage."""


class ResponseExtractionError(Exception):
    """Raised when there is an issue extracting information from the model's response."""
