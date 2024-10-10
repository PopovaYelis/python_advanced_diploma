from typing import Optional

from pydantic import BaseModel



class UserSchema(BaseModel):
    id: int
    name: str
    api_key: str


class UserOutSchema(UserSchema):
    class Config:
        orm_mode = True

