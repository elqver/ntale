import httpx

from pydantic import BaseModel


class City(BaseModel):
    name: str
    latitude: float
    longitude: float
    country: str
    population: int
    is_capital: bool


async def get_city_info(en_city_name: str, ninja_api_key: str) -> City | None:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://api.api-ninjas.com/v1/city",
            params={"name": en_city_name, "units": "metric"},
            headers={"X-Api-Key": ninja_api_key},
        )
        cities = r.json()
        if not cities:
            return None
        return City(**cities[0])
