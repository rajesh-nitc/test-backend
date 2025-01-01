from services.api.spend import get_spend
from services.api.weather import get_location_coordinates, get_weather_by_coordinates
from services.search.toys import search_toys

# A registry of available functions and their handlers
FUNCTION_REGISTRY = {
    "get_spend_func": get_spend,
    "search_toys_func": search_toys,
    "get_location_coordinates_func": get_location_coordinates,
    "get_weather_by_coordinates_func": get_weather_by_coordinates,
}
