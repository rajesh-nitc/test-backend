def get_datapoint_ids(response, top_k):
    """
    Extracts datapoint IDs from the Vertex AI vector index response.

    Args:
        response (FindNeighborsResponse): The response from Vertex AI Vector Index.
        top_k (int): Number of top nearest neighbors to retrieve.

    Returns:
        list: List of datapoint IDs of the top_k nearest neighbors.
    """
    # Check if nearest_neighbors is present
    if not response.nearest_neighbors:
        raise ValueError("Invalid response: 'nearest_neighbors' field is empty.")

    # Extract neighbors for the first query (assuming single query for simplicity)
    neighbors = response.nearest_neighbors[0].neighbors

    # Extract datapoint IDs for top_k neighbors
    datapoint_ids = [neighbor.datapoint.datapoint_id for neighbor in neighbors[:top_k]]

    return datapoint_ids
