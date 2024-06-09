import httpx
from pydantic import BaseModel


class Weather(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class Temperature(BaseModel):
    morn: float
    day: float
    eve: float
    night: float
    min: float
    max: float


class FeelsLike(BaseModel):
    morn: float
    day: float
    eve: float
    night: float


class DailyForecast(BaseModel):
    dt: int
    sunrise: int | None
    sunset: int | None
    moonrise: int
    moonset: int
    moon_phase: float
    summary: str
    temp: Temperature
    feels_like: FeelsLike
    pressure: int
    humidity: int
    dew_point: float
    wind_speed: float
    wind_gust: float | None = None
    wind_deg: int
    clouds: int
    uvi: float
    pop: float
    rain: float | None = None
    snow: float | None = None
    weather: list[Weather]


async def get_tomorrow_weather(
    lat: float, lon: float, open_weather_api_key: str
) -> DailyForecast:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://api.openweathermap.org/data/3.0/onecall",
            params={
                "cnt": 1,
                "lat": lat,
                "lon": lon,
                "appid": open_weather_api_key,
                "exclude": "current,minutely,hourly,alerts",
                "units": "metric",
            },
        )
        return DailyForecast(**r.json()["daily"][1])
