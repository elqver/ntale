# NeuroTale

![Logo](./ntale.jpg)

## Description
NeuroTale is a simple project designed to provide hands-on experience with fancy large language model (LLM) APIs such as YandexGPT and GigaChat.

## How to Use

You can run NeuroTale in three ways:
- As a console script
- In a Docker container
- Using the hosted version

### As a Console Script

1. **Clone this repository:**
    ```sh
    git clone https://github.com/elqver/ntale && cd ntale
    ```

2. **Create a virtual environment and install dependencies:**
    ```sh
    python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
    ```

3. **Obtain the necessary API keys and tokens:**
    - [Ninja API Key](https://api-ninjas.com/profile) should be added as `NINJA_API_KEY`
    - [Google Cloud API Key](https://console.cloud.google.com/apis/credentials) should be added as `GOOGLE_CLOUD_API_KEY`
    - [OpenWeather API Key](https://home.openweathermap.org/api_keys) should be added as `OPEN_WEATHER_API_KEY`
    - [Yandex Catalog ID](https://console.yandex.cloud/) should be added as `YANDEX_CATALOG_ID`
    - [Yandex OAuth Token](https://yandex.cloud/en/docs/iam/concepts/authorization/oauth-token) should be added as `YANDEX_OAUTH_TOKEN`
    - For GigaChat (Sber), the following environment variables are required:
        - `GIGA_CLIENT_ID`
        - `GIGA_CLIENT_SECRET`
        - `GIGA_AUTH_DATA`
        - `GIGA_SCOPE`

4. **Select a path for storing tales and logs:**
    ```sh
    SHARED_PATH="storage"
    ```

5. **Save the environment variables:**
    Save the API keys and tokens in an `.env` file in the same directory.

6. **Run the script:**
    Call the script with three parameters:
    1. City to get the weather-tale
    2. Genre of the tale
    3. Upper boundary for the amount of tokens in the tale
    ```sh
    source venv/bin/activate && env $(cat .env | xargs) python app/main.py Moscow Action 2000
    ```

### Inside a Docker Container

You can run script inside docker container. 
It will get you rid of interpreter and packages dependencies problems, 
but you are still the one to provide and setup all API tokens.


1. **Clone this repository:**
    ```sh
    git clone https://github.com/elqver/ntale && cd ntale
    ```

2. **Create .env file:**
    ```sh
    NINJA_API_KEY=
    GOOGLE_CLOUD_API_KEY=
    OPEN_WEATHER_API_KEY=
    YANDEX_CATALOG_ID=
    YANDEX_OAUTH_TOKEN=
    GIGA_CLIENT_ID=
    GIGA_CLIENT_SECRET=
    GIGA_AUTH_DATA=
    GIGA_SCOPE=
    SHARED_PATH=storage
    ```

3. **Build docker image**
    ```sh
    docker build -t neurotale .
    ```

4. **And run container**
    ```sh
    docker run --env-file .env -v "$(pwd)/storage:/app/storage" neurotale Saratov Action 2000
    ```

### Just play with hosted version

You can just go `http://45.145.6.50:8000/docs`
This is suitable because you don't need run any software or collect API tokens by youreself.
By the way you alse can checkout `web-port` branch and host web version by yourself.
Instructions are the same as for first two variants except for target file: `web_app.py`.

**CARE**: 

Endpoints are deffenetly not safe! 
Don't expose it to WAN on machines with sensetive information!
