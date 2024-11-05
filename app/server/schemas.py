from typing import Optional, List

from pydantic import BaseModel



class UserSchema(BaseModel):
    id: int
    name: str
    api_key: str


class UserOutSchema(UserSchema):
    class Config:
        from_attributes = True

class TweetSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]]