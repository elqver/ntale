# NeuroTale

TODO: add logo here


## Description:
This is just a simple project to get hands on those fancy llm apis:

YandexGPT and GigaChat used

## How to use:

You can run this: 
    - As a console script
    - In docker container
    - Just play with hosted version


### As a console script

1. Clone this repo with git:

```git clone https://github.com/elqver/ntale && cd ntale```

2. Create virtual env and install dependencies:

```python -m venv venv && source venv/bin/actiavte && pip install -r requirements.txt```

3. Get all those nasty tokens

[API key for Ninja API](https://api-ninjas.com/profile)
should be added as `NINJA_API_KEY`

[Google cloud api key](https://console.cloud.google.com/apis/credentials)
should be added as `GOOGLE_CLOUD_API_KEY`

[Open weather API key](https://home.openweathermap.org/api_keys)
should be added as `OPEN_WEATHER_API_KEY`

[Yandex catatlog id](https://console.yandex.cloud/)
should be added as `YANDEX_CATALOG_ID`

[Yandex oauth token](https://yandex.cloud/en/docs/iam/concepts/authorization/oauth-token
should be added as `YANDEX_OAUTH_TOKEN`

[For GigaChat Sber](https://developers.sber.ru/docs/ru/gigachat/individuals-quickstart) 
following envs are required to be added:
`GIGA_CLIENT_ID`
`GIGA_CLIENT_SECRET`
`GIGA_AUTH_DATA`
`GIGA_SCOPE`

4. Select path for tales and logs storage

for example:
```SHARED_PATH="storage"```

5. Save those envs somewhere, for example in `.env` file in the same directory

6. Finaly you can call this script with three params:
1) City to get weather-tale
2) Genre of a tale
3) Upper boundary for amount of tokens in tale

```source venv/bin/activate && env $(cat .env | xargs) python app/main.py Moscow Action 2000```


### Inside a container
