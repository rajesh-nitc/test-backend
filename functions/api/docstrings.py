from utils.date import get_today_date
from utils.text import dedent_and_strip

date, day_of_week = get_today_date()

spend = dedent_and_strip(
    f"""
    Extract the category, start_date, and end_date from user queries.
    Today's date is {date} ({day_of_week}). Handle relative terms like "last year" or "this month".
    Example usage:
    - What were my expenses this year?: category is None, start_date is YYYY-01-01, end_date is today's date
    - How much did I spend on groceries last year?: category is groceries, start_date is YYYY-01-01, end_date is YYYY-12-31
    - What were my expenses in January?: category is None, start_date is YYYY-01-01, end_date is YYYY-01-31
    """
)

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
    Example usage:
    - Get weather for lat=12.9716 and lon=77.5946
"""
)
