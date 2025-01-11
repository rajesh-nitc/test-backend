from config.settings import settings
from functions.api.spend import get_spend_func
from functions.api.weather import (
    get_location_coordinates_func,
    get_weather_by_coordinates_func,
)
from functions.search.toys import search_toys_func
from services.api.spend import get_spend
from services.api.weather import get_location_coordinates, get_weather_by_coordinates
from services.search.toys import search_toys
from utils.agent import Agent

# A registry of available functions and their handlers
FUNCTION_REGISTRY = {
    "get_spend_func": get_spend,
    "search_toys_func": search_toys,
    "get_location_coordinates_func": get_location_coordinates,
    "get_weather_by_coordinates_func": get_weather_by_coordinates,
}


def get_agent() -> Agent:
    return Agent(
        name=f"{settings.APP_NAME}-agent",
        model=settings.LLM_MODEL,
        system_instruction=settings.LLM_SYSTEM_INSTRUCTION,
        functions=[
            get_location_coordinates_func,
            get_weather_by_coordinates_func,
            get_spend_func,
            search_toys_func,
        ],
    )
