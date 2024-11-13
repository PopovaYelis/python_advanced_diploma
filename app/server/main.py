"""Main application file."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from database import engine
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api")

# app.mount("/images", StaticFiles(directory="/server/images"), name="images")