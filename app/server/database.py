import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

def get_database_url() -> str:
    if os.environ.get("ENV") == "test":
        url_engine = os.getenv("DATABASE_URL_TEST")
    else:
        url_engine = os.getenv("DATABASE_URL")

    return url_engine

engine = create_async_engine(get_database_url(), echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
session = async_session()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
