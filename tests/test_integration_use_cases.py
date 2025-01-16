import asyncio

import pytest
from fastapi.testclient import TestClient  # type: ignore

from main import app

client = TestClient(app)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_use_cases_concurrent(test_use_cases):  # Inject the fixture here
    """Test use cases concurrently."""

    async def make_api_call(prompt, user_id, expected_keywords, check_function):
        payload = {
            "prompt": prompt,
            "user_id": user_id,
        }
        response = client.post("api/prompt", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "response" in data  # Ensure 'response' key exists

        # Use the appropriate check function for the test case
        assert check_function(
            data["response"], expected_keywords
        ), f"Response '{data['response']}' does not meet the expected keyword criteria."

    # Create a list of tasks to run concurrently
    tasks = [
        make_api_call(
            test_case["prompt"],
            test_case["user_id"],
            test_case["expected_keywords"],
            test_case["check_function"],
        )
        for test_case in test_use_cases
    ]

    # Run the requests concurrently
    await asyncio.gather(*tasks)
