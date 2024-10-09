from fastapi import APIRouter, FastAPI, HTTPException
from sqlalchemy import delete, update
from schemas import UserOutSchema
from typing import List
from database import engine, session
from models import Cats, Base
from sqlalchemy.future import select
router = APIRouter()


@router.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


