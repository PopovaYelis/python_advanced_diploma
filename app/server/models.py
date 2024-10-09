from pydoc import describe

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
)
from typing import Dict, Any
from database import Base, session

class Cats(Base):
    __tablename__ = 'cats'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    api_key: Mapped[str] = mapped_column(String, unique=True, index=True)