import os
from pathlib import Path


from loguru import logger


def get_env_variable(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"No {key} provided")
    return value


NINJA_API_KEY: str = get_env_variable("NINJA_API_KEY")
GOOGLE_CLOUD_API_KEY: str = get_env_variable("GOOGLE_CLOUD_API_KEY")
OPEN_WEATHER_API_KEY: str = get_env_variable("OPEN_WEATHER_API_KEY")
YANDEX_CATALOG_ID: str = get_env_variable("YANDEX_CATALOG_ID")
YANDEX_OAUTH_TOKEN: str = get_env_variable("YANDEX_OAUTH_TOKEN")
GIGA_AUTH_DATA: str = get_env_variable("GIGA_AUTH_DATA")
GIGA_SCOPE: str = get_env_variable("GIGA_SCOPE")
SHARED_PATH = Path(get_env_variable("SHARED_PATH"))


def setup_logging():
    logger.remove()
    logger.add(SHARED_PATH / "logs.log")
