"""Schemas for routes."""
from typing import List, Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    Schema for user data.

    id(int): user id
    name(str): user name

    """

    id: int
    name: str


class UserOutSchema(UserSchema):
    """
    Schema for output user data.

    followers(array): followers
    following(array): following
    """

    followers: List[UserSchema]
    following: List[UserSchema]

    class Config:
        """
        Configuration settings for Pydantic models.

        from_attributes(bool)
        """

        from_attributes = True


class TweetSchema(BaseModel):
    """
    Schema for tweet data.

    tweet_data(str): content_data of tweet
    tweet_media_ids(array): id from media
    """

    tweet_data: str
    tweet_media_ids: Optional[List[int]]
