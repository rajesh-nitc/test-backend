from functions.api.docstrings import coordinates, weather


def get_location_coordinates_func(location: str) -> dict:
    return {"lat": float, "lon": float}


def get_weather_by_coordinates_func(lat: float, lon: float) -> dict:
    return {"data": "data"}


get_location_coordinates_func.__doc__ = coordinates
get_weather_by_coordinates_func.__doc__ = weather
