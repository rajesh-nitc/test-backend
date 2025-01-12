from utils.text import dedent_and_strip

coordinates = dedent_and_strip(
    """
    Retrieves the latitude and longitude of a given location using OpenWeather's Geocoding API.
    Example usage:
    - weather in Bengaluru: location is Bengaluru,IN. Use ISO 3166-1 alpha-2 country codes.
    - weather in New York: location is New York,NY,US. City name, state code (only for the US) and country code divided by comma.
    """
)

weather = dedent_and_strip(
    """
    Retrieves the current weather details for a given location based on latitude and longitude using OpenWeather's Weather API.
    Convert the temperature from Kelvin to Celsius using the formula: Celsius = Kelvin - 273.15. Return the result in Celsius.
"""
)
