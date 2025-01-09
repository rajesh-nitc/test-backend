import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--test-cases",
        action="store",
        default="",  # "weather,spend,toys" # default is don't run any
        help="Comma-separated list of test case names to run, e.g., 'weather,spend,toys'",
    )


@pytest.fixture
def test_use_cases(request):
    all_cases = {
        "weather": {
            "prompt": "how is the weather in bengaluru and mumbai?",
            "user_id": "test_user_1",
            "expected_keywords": ["bengaluru", "mumbai"],
        },
        "spend": {
            "prompt": "how much did i spend on entertainment this year?",
            "user_id": "test_user_2",
            "expected_keywords": ["spent", "entertainment"],
        },
        "toys": {
            "prompt": "suggest toys like Uno under $25?",
            "user_id": "test_user_3",
            "expected_keywords": ["toy", "toys"],
        },
    }
    selected_tests = request.config.getoption("--test-cases").split(",")
    return [all_cases[test] for test in selected_tests if test in all_cases]
