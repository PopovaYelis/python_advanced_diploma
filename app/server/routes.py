from fastapi import APIRouter, FastAPI, HTTPException, Header
from sqlalchemy import delete, update
from schemas import UserOutSchema
from typing import List
from database import engine, session
from models import User, Base
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
router = APIRouter()


query_params = {"api_key": "test"}

@router.get(
    path="/users/me",
    response_model=UserOutSchema,
)
async def get_profile_my(
) -> UserOutSchema:
    """
    Получить профиль текущего пользователя.

    Параметры:
        session (AsyncSession): Сессия базы данных.
        api_key (str): API ключ пользователя, передаваемый в заголовке.

    Возвращает:
        SuccessOutUserSchema: Данные профиля пользователя.

    """
    user_select = await session.execute(
        select(User)
        .where(User.api_key == query_params["api_key"])
    )
    result =  user_select.scalar()
    return result
