from unittest.mock import Mock

# Import the function to test
from utils.llm import extract_function_call


def test_extract_function_call_valid_response():
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

    result = extract_function_call(response_mock)
    assert result == {
        "get_spend_func": {
            "start_date": "2024-11-01",
            "end_date": "2024-11-30",
            "category": "groceries",
        }
    }


def test_extract_function_call_no_function_calls():
    """Test with a response that has no function calls."""
    candidate_mock = Mock()
    candidate_mock.function_calls = []

    response_mock = Mock()
    response_mock.candidates = [candidate_mock]

    result = extract_function_call(response_mock)
    assert result == {}
