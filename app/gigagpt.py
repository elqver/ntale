from datetime import datetime

import uuid
import httpx


class GigaToken:
    def __init__(self, auth_data: str, scope: str) -> None:
        self.scope = scope
        self._auth_data = auth_data
        self._token: str = ""
        self._expires_at: float = 0

    async def get_token(self) -> str:
        rqUID = str(uuid.uuid4())
        if self._token and datetime.now().timestamp() < self._expires_at:
            return self._token

        # TODO:
        # The hell why sber has problems with ssl?
        # verify_ssl_certs=False even in docuemntation for their SDK:
        # https://developers.sber.ru/docs/ru/gigachat/individuals-quickstart?tool=python
        # verify=False should be removed later on
        async with httpx.AsyncClient(verify=False) as client:
            r = await client.post(
                "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
                data={"scope": self.scope},
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                    "RqUID": rqUID,
                    "Authorization": f"Basic {self._auth_data}",
                },
            )
            r.raise_for_status()
            r = r.json()
            self._token = r["access_token"]
            self._expires_at = r["expires_at"]
        return self._token

    def __await__(self):
        return self.get_token().__await__()


async def list_models(token: GigaToken):
    # TODO:
    async with httpx.AsyncClient(verify=False) as client:
        return (
            (
                await client.get(
                    "https://gigachat.devices.sberbank.ru/api/v1/models",
                    headers={
                        "Authorization": f"Bearer {await token}",
                    },
                )
            )
            .raise_for_status()
            .json()
        )


async def request_gpt(
    token: GigaToken,
    max_tokens: int,
    instructions: str,
    request: str,
    temperature: float = 0.2,
    top_p: float = 0.1,
    repetition_penalty: float = 1.0,
):
    # TODO:
    async with httpx.AsyncClient(verify=False) as client:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {await token}",
        }
        data = {
            "model": "GigaChat",
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "n": 1,
            "repetition_penalty": repetition_penalty,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": instructions,
                },
                {
                    "role": "user",
                    "content": request,
                },
            ],
        }
        return (
            await client.post(
                "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60,
            )
        ).json()["choices"][0]["message"]["content"]
