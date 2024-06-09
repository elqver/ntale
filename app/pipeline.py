from typing import Literal

from city import get_city_info
from setup import (
    GIGA_AUTH_DATA,
    GIGA_SCOPE,
    GOOGLE_CLOUD_API_KEY,
    NINJA_API_KEY,
    OPEN_WEATHER_API_KEY,
    YANDEX_OAUTH_TOKEN,
    YANDEX_CATALOG_ID,
)
from translate import get_en_city_name, get_ru_city_name
from weather import DailyForecast, get_tomorrow_weather
from yandexgpt import IamToken, request_gpt as yandex_request_gpt
from gigagpt import GigaToken, request_gpt as giga_request_gpt
from prompts import genre_prompts, weather_humanize_prompt
from time_utils import log_exectuion_time

iam_token = IamToken(YANDEX_OAUTH_TOKEN)
giga_token = GigaToken(GIGA_AUTH_DATA, GIGA_SCOPE)


@log_exectuion_time
async def generate_giga_tale(
    genre: str, ru_city_name: str, weather: str, tokens_amount: int
):
    return await giga_request_gpt(
        token=giga_token,
        max_tokens=tokens_amount,
        instructions=genre_prompts[genre].format(city=ru_city_name),
        request=weather,
        temperature=0.2,
    )


@log_exectuion_time
async def humanize_weather_giga(weather: DailyForecast):
    return await giga_request_gpt(
        token=giga_token,
        max_tokens=2000,
        instructions=weather_humanize_prompt,
        request=str(weather),
        temperature=0.05,
    )


@log_exectuion_time
async def generate_yandex_tale(
    genre: str, ru_city_name: str, weather: str, tokens_amount: int
):
    return await yandex_request_gpt(
        catalog_id=YANDEX_CATALOG_ID,
        iam_token=iam_token,
        max_tokens=tokens_amount,
        instructions=genre_prompts[genre].format(city=ru_city_name),
        request=weather,
        temperature=0.2,
    )


@log_exectuion_time
async def humanize_weather_yandex(weather: DailyForecast):
    return await yandex_request_gpt(
        catalog_id=YANDEX_CATALOG_ID,
        iam_token=iam_token,
        max_tokens=2000,
        instructions=weather_humanize_prompt,
        request=str(weather),
        temperature=0.05,
    )


@log_exectuion_time
async def get_weather_by_city(city: str):
    en_city = await get_en_city_name(city, GOOGLE_CLOUD_API_KEY)
    city_info = await get_city_info(en_city, NINJA_API_KEY)
    if city_info is None:
        raise ValueError(f"No info about city: {city}")
    return await get_tomorrow_weather(
        lat=city_info.latitude,
        lon=city_info.longitude,
        open_weather_api_key=OPEN_WEATHER_API_KEY,
    )


@log_exectuion_time
async def generate_tale(
    backend: Literal["yandex", "giga"],
    city: str,
    genre: str,
    tokens_amount: int,
):
    weahter_humanizer = {
        "yandex": humanize_weather_yandex,
        "giga": humanize_weather_giga,
    }[backend]
    tale_generator = {
        "yandex": generate_yandex_tale,
        "giga": generate_giga_tale,
    }[backend]

    ru_city_name = await get_ru_city_name(city, GOOGLE_CLOUD_API_KEY)
    get_weather_data = await get_weather_by_city(city)
    humanized_weather = await weahter_humanizer(get_weather_data)
    return await tale_generator(
        genre,
        ru_city_name,
        humanized_weather,
        tokens_amount,
    )
