"""Database."""

import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


def get_database_url() -> str:
    """
    Get url for database.

    Returns:
        url (str): url for database.
    """
    if os.environ.get('ENV') == 'test':
        url_engine = os.getenv('DATABASE_URL_TEST')
    else:
        url_engine = os.getenv('DATABASE_URL')
    return url_engine


engine = create_async_engine(get_database_url(), echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
session = async_session()
