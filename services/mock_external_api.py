import logging
logger = logging.getLogger(__name__)
def fetch_mock_data(params: dict = None) -> dict:
    """Mock function to return hardcoded data."""
    
    logger.info(f"Received params from Model: {params}")
    
    return {
        "data": {"amount": "$25"}
    }
