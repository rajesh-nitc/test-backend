from services.api_spend import get_spend
from services.search_toys import search_toys

# A registry of available functions and their handlers
FUNCTION_REGISTRY = {
    "get_spend_func": get_spend,
    "search_toys_func": search_toys,
}
