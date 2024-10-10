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
)
async def get_profile_my(
):

    user_select = await session.execute(
        select(User)
        .where(User.api_key == query_params["api_key"])
    )
    result =  user_select.scalar()
    res = {
        "result": "true",
        "user": {
            "id": "int",
            "name": result.name,
            "followers": [
                {
                    "id": 1,
                    "name": 'lisa'
                }
            ],
            "following": [
                {
                    "id": 1,
                    "name": "lisa1"
                }
            ]
        }
    }

    return res
