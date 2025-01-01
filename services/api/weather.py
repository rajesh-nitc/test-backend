import logging

from models.api.weather import OpenWeatherGeocodingRequestData, OpenWeatherRequestData
from utils.http import HTTPClientSingleton

logger = logging.getLogger(__name__)


async def get_location_coordinates(function_args: dict) -> list[dict]:
    """
    Get location coordinates from OpenWeather Geocoding API
    """

    try:
        model_instance = OpenWeatherGeocodingRequestData.model_validate(function_args)
        logger.info(model_instance.model_dump())
        client = HTTPClientSingleton.get_instance()
        response = await client.get(
            "/geo/1.0/direct",
            params={"q": model_instance.location, "appid": model_instance.appid},
        )
        logger.info(f"api_response: {response.text}")
        response.raise_for_status()
        data = response.json()
        return data

    except Exception as e:
        logger.error(e)
        return [{"error": "An error occurred, please try again later."}]


async def get_weather_by_coordinates(function_args: dict) -> dict:
    """
    Get weather data from coordinates using OpenWeather Weather API
    """

    try:
        model_instance = OpenWeatherRequestData.model_validate(function_args)
        logger.info(model_instance.model_dump())
        client = HTTPClientSingleton.get_instance()
        response = await client.get(
            "/data/2.5/weather",
            params={
                "lat": model_instance.lat,
                "lon": model_instance.lon,
                "appid": model_instance.appid,
            },
        )
        logger.info(f"api_response: {response.text}")
        response.raise_for_status()
        data = response.json()
        return data

    except Exception as e:
        logger.error(e)
        return {"error": "An error occurred, please try again later."}
