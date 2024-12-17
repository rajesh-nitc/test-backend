from services.spend_api import get_spend
from services.toy_search import get_toys

# A registry of available functions and their handlers
FUNCTION_REGISTRY = {
    "get_spend_func": get_spend,
    "get_toys_func": get_toys,
}
