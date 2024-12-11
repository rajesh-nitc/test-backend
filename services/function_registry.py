from services.spend import get_spend

# A registry of available functions and their handlers
FUNCTION_REGISTRY = {
    "get_spend_func": get_spend,
}
