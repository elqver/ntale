from datetime import datetime, timezone
import httpx


class IamToken:
    def __init__(self, oauth: str) -> None:
        self._oauth: str = oauth
        self._iam_token: str = ""
        self._iam_expires_at: float = 0

    async def get_iam_token(self) -> str:
        if self._iam_token and datetime.now().timestamp() < self._iam_expires_at:
            return self._iam_token

        async with httpx.AsyncClient() as client:
            r = await client.post(
                "https://iam.api.cloud.yandex.net/iam/v1/tokens",
                json={"yandexPassportOauthToken": self._oauth},
                headers={
                    "Content-Type": "application/json",
                },
            )
            self._iam_token: str = r.json()["iamToken"]
            expair_iso: str = r.raise_for_status().json()["expiresAt"][:26]
            self._iam_expires_at: float = (
                datetime.fromisoformat(expair_iso)
                .replace(tzinfo=timezone.utc)
                .timestamp()
            )

        return self._iam_token

    def __await__(self):
        return self.get_iam_token().__await__()


async def request_gpt(
    catalog_id: str,
    iam_token: IamToken,
    max_tokens: int,
    instructions: str,
    request: str,
    temperature: float = 0.2,
) -> str:
    async with httpx.AsyncClient() as client:
        json_prompt = {
            "modelUri": f"gpt://{catalog_id}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": temperature,
                "maxTokens": str(max_tokens),
            },
            "messages": [
                {
                    "role": "system",
                    "text": instructions,
                },
                {
                    "role": "user",
                    "text": request,
                },
            ],
        }
        r = await client.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
            json=json_prompt,
            headers={
                "Authorization": f"Bearer {await iam_token}",
                "x-folder-id": catalog_id,
                "Content-Type": "application/json",
            },
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["result"]["alternatives"][0]["message"]["text"]
