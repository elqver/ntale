import httpx


async def translate(q: str, target: str, google_cloud_api_key: str) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://translation.googleapis.com/language/translate/v2",
            params={
                "q": q,
                "target": target,
                "format": "text",
                "key": google_cloud_api_key,
            },
        )
        return r.json()["data"]["translations"][0]["translatedText"]


async def get_en_city_name(name: str, key: str) -> str:
    return await translate(name, "en", key)


async def get_ru_city_name(name: str, key: str) -> str:
    return await translate(name, "ru", key)
