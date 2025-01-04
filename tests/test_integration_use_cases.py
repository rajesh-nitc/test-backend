import asyncio

import pytest
from fastapi.testclient import TestClient  # type: ignore

from main import app

client = TestClient(app)

test_use_cases = [
    {
        "prompt": "how is the weather in bengaluru and mumbai?",
        "user_id": "test_user_1",
        "expected_keywords": ["bengaluru", "mumbai"],
    },
    {
        "prompt": "how much did i spend on entertainment this year?",
        "user_id": "test_user_2",
        "expected_keywords": ["spent", "entertainment"],
    },
    {
        "prompt": "suggest toys like Uno under $25?",
        "user_id": "test_user_3",
        "expected_keywords": ["toys"],
    },
]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_use_cases_concurrent():
    """Test use cases concurrently."""

    async def make_api_call(prompt, user_id, expected_keywords):
        payload = {
            "prompt": prompt,
            "user_id": user_id,
        }
        response = client.post("api/prompt", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "response" in data  # Ensure 'response' key exists

        # Check if the correct keywords are in the response
        for keyword in expected_keywords:
            assert keyword in data["response"].lower()

    # Create a list of tasks to run concurrently
    tasks = [
        make_api_call(
            test_case["prompt"], test_case["user_id"], test_case["expected_keywords"]
        )
        for test_case in test_use_cases
    ]

    # Run the requests concurrently
    await asyncio.gather(*tasks)
