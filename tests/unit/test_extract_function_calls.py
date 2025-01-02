from unittest.mock import Mock

# Import the function to test
from config.exceptions import ResponseExtractionError
from utils.llm import extract_function_calls


def test_extract_function_calls_valid_response():
    """Test with a valid response containing a function call."""
    function_call_mock = Mock()
    function_call_mock.name = "get_spend_func"
    function_call_mock.args = {
        "start_date": "2024-11-01",
        "end_date": "2024-11-30",
        "category": "groceries",
    }

    candidate_mock = Mock()
    candidate_mock.function_calls = [function_call_mock]

    response_mock = Mock()
    response_mock.candidates = [candidate_mock]

    result = extract_function_calls(response_mock)
    assert result == [
        {
            "get_spend_func": {
                "start_date": "2024-11-01",
                "end_date": "2024-11-30",
                "category": "groceries",
            }
        }
    ]


def test_extract_function_calls_no_function_calls():
    """Test with a response that has no function calls."""
    candidate_mock = Mock()
    candidate_mock.function_calls = []

    response_mock = Mock()
    response_mock.candidates = [candidate_mock]

    result = extract_function_calls(response_mock)
    assert result == []


def test_extract_function_calls_exception_handling():
    """Test exception handling when response format is invalid."""
    response_mock = Mock()
    response_mock.candidates = None  # Invalid format

    try:
        extract_function_calls(response_mock)
        assert False, "Expected ResponseExtractionError to be raised"
    except ResponseExtractionError:
        pass  # Exception was correctly raised
