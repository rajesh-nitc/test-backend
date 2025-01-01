from vertexai.generative_models import FunctionDeclaration

DESCRIPTIONS_COORDINATES = {
    "FUNCTION": """
Retrieves the latitude and longitude of a given location using OpenWeather's Geocoding API.
Example usage:
    - weather in Bengaluru: location is Bengaluru,IN
    - weather in New York: location is New York,NY,US
""",
    "location": """
City name, state code (only for the US) and country code divided by comma. Please use ISO 3166-1 alpha-2 country codes.
""",
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
    "FUNCTION": """
Retrieves the current weather details for a given location based on latitude and longitude using OpenWeather's Weather API.
Example usage:
    - Get weather for lat=12.9716 and long=77.5946 (Bengaluru, IN)
""",
    "latitude": "The latitude of the location.",
    "longitude": "The longitude of the location.",
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
