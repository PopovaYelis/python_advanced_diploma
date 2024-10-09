from typing import Optional

from pydantic import BaseModel



class UserSchema(BaseModel):
    """
    Базовая схема пользователя.

    Атрибуты:
        id (int): Идентификатор пользователя.
        name (str): Имя пользователя.
    """

    id: int
    name: str
    api_key: str


class UserOutSchema(UserSchema):
    class Config:
        orm_mode = True

