from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_prompt():
    """Test a request to the prompt endpoint with a real API call to Gemini."""
    payload = {
        "prompt": "how much did i spend on travel last month",
        "user_id": "rajesh-nitc",
    }
    response = client.post("api/v1/prompt", json=payload)

    # Print the response for debugging
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "response" in data  # Ensure 'response' key exists

    # Check if the response contains expected elements, like "spent" and "travel"
    assert "spent" in data["response"].lower()  # Ensure the response mentions 'spent'
    assert "travel" in data["response"].lower()  # Ensure the response mentions 'travel'
