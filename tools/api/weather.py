from vertexai.generative_models import FunctionDeclaration

from utils.text import dedent_and_strip

DESCRIPTIONS_COORDINATES = {
    "FUNCTION": dedent_and_strip(
        """
Retrieves the latitude and longitude of a given location using OpenWeather's Geocoding API.
Example usage:
    - weather in Bengaluru: location is Bengaluru,IN
    - weather in New York: location is New York,NY,US
"""
    ),
    "location": dedent_and_strip(
        """
City name, state code (only for the US) and country code divided by comma.
Use ISO 3166-1 alpha-2 country codes.
"""
    ),
}

# Define the function declaration
get_location_coordinates_func = FunctionDeclaration(
    name="get_location_coordinates_func",
    description=DESCRIPTIONS_COORDINATES["FUNCTION"],
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": DESCRIPTIONS_COORDINATES["location"],
            },
        },
        "required": ["location"],
    },
)

DESCRIPTIONS_WEATHER = {
    "FUNCTION": dedent_and_strip(
        """
Retrieves the current weather details for a given location based on latitude and longitude using OpenWeather's Weather API.
Example usage:
    - Get weather for lat=12.9716 and lon=77.5946
"""
    ),
    "latitude": dedent_and_strip(
        """
Latitude
"""
    ),
    "longitude": dedent_and_strip(
        """
Longitude
"""
    ),
}

# Define the function declaration
get_weather_by_coordinates_func = FunctionDeclaration(
    name="get_weather_by_coordinates_func",
    description=DESCRIPTIONS_WEATHER["FUNCTION"],
    parameters={
        "type": "object",
        "properties": {
            "lat": {
                "type": "number",
                "description": DESCRIPTIONS_WEATHER["latitude"],
            },
            "lon": {
                "type": "number",
                "description": DESCRIPTIONS_WEATHER["longitude"],
            },
        },
        "required": ["lat", "lon"],
    },
)
