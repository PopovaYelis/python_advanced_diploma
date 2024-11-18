"""Main application file."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from database import engine
from fastapi import FastAPI
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: This will yield control back to the FastAPI application.
    """
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix='/api')
