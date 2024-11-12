from typing import Optional, List

from pydantic import BaseModel



class UserSchema(BaseModel):
    id: int
    name: str


class UserOutSchema(UserSchema):


    followers: list[UserSchema]
    following: list[UserSchema]

    class Config:
        from_attributes = True


class TweetSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]]