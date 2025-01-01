from vertexai.generative_models import Tool

from tools.api.spend import get_spend_func
from tools.api.weather import (
    get_location_coordinates_func,
    get_weather_by_coordinates_func,
)
from tools.search.toys import search_toys_func

tool = Tool(
    function_declarations=[
        get_spend_func,
        search_toys_func,
        get_location_coordinates_func,
        get_weather_by_coordinates_func,
    ],
)
