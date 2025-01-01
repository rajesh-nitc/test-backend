from pydantic import BaseModel

from config.settings import settings


class OpenWeatherGeocodingRequestData(BaseModel):
    location: str
    appid: str = settings.OPENWEATHER_API_KEY
    limit: int | None = None


class OpenWeatherRequestData(BaseModel):
    lat: float
    lon: float
    appid: str = settings.OPENWEATHER_API_KEY
    exclude: str | None = None
