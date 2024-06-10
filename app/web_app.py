import os
import asyncio
from typing import Literal
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from pipeline import generate_tale
from file_utils import save_to_file
from setup import SHARED_PATH, setup_logging


app = FastAPI()


class TaleRequest(BaseModel):
    city: str
    genre: Literal["Drama", "Comedy", "Musical", "Detective", "Action", "Horror"]
    length: int = 2000


@app.get("/logs")
async def get_logs():
    try:
        return FileResponse(SHARED_PATH / "logs.log")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tales")
async def list_tales():
    try:
        return os.listdir(SHARED_PATH / "tales")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tales/{file_name}")
async def read_tale(file_name: str):
    try:
        return FileResponse(SHARED_PATH / "tales" / file_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tales")
async def create_tale(request: TaleRequest):
    try:
        yandex_tale, giga_tale = await asyncio.gather(
            generate_tale("yandex", request.city, request.genre, request.length),
            generate_tale("giga", request.city, request.genre, request.length),
        )
        postfix = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
        yandex_tale_path = SHARED_PATH / f"tales/yandex_tale_{postfix}.txt"
        giga_tale_path = SHARED_PATH / f"tales/giga_tale_{postfix}.txt"
        save_to_file(yandex_tale_path, yandex_tale)
        save_to_file(giga_tale_path, giga_tale)
        return {
            "yandex": f"yandex_tale_{postfix}.txt",
            "giga": f"giga_tale_{postfix}.txt",
        }
    except asyncio.TimeoutError:
        raise HTTPException(status_code=503, detail="Service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    setup_logging()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
