from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI, status

from core import SessionLocal
from pre_start import create_admin
from task_api import task_router
from user_api import user_router
from auth_api import auth_router


@asynccontextmanager
async def lifespan_on_start_app(app: FastAPI) -> AsyncIterator[None]:
    async with SessionLocal() as session:
        await create_admin(session)

    yield


app = FastAPI(lifespan=lifespan_on_start_app)


app.include_router(task_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
async def health():
    return status.HTTP_200_OK
