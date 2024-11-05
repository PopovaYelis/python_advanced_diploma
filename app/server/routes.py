import json
import os

from fastapi import APIRouter, FastAPI, HTTPException, Header, Request, UploadFile, File
from sqlalchemy import delete, update
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError
import aiofiles
from schemas import UserOutSchema
from typing import List
from database import engine, session
from models import User, Base, Tweet, Like, Follow, Media
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import TweetSchema
import logging
router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get(path="/users/me")
async def get_profile_my(api_key: str = Header(default=..., alias="api-key")):
    user_select = await session.execute(
        select(User)
        .where(User.api_key == api_key)
    )
    result = user_select.scalar()
    followers_d = await session.execute(select(Follow).where(Follow.followed_id == result.id))
    followers_data = followers_d.scalars()
    followers_list = []
    for followers in followers_data:
        name_user = await session.execute(select(User).where(User.id == followers.follower_id))
        name = name_user.scalar()
        followers_list.append({"id": followers.follower_id,
                               "name": name.name})
    followed_d = await session.execute(select(Follow).where(Follow.follower_id == result.id))
    followed_data = followed_d.scalars()
    followed_list = []
    for followed in followed_data:
        name_user = await session.execute(select(User).where(User.id == followed.followed_id))
        name = name_user.scalar()
        followed_list.append({"id": followed.followed_id,
                              "name": name.name})

    res = {
        "result": "true",
        "user": {
            "id": result.id,
            "name": result.name,
            "followers": followers_list,
            "following": followed_list
        }
    }

    return res


@router.post(path="/tweets")
async def tweet_post(tweet_data: TweetSchema, api_key: str = Header(default=..., alias="api-key")):
    user_select = await session.execute(
        select(User)
        .where(User.api_key == api_key)
    )
    user = user_select.scalar()
    if user:
        user_id = user.id

        tweet_model = Tweet(content=tweet_data.tweet_data, attachments=tweet_data.tweet_media_ids, user_id = user_id)

        session.add(tweet_model)
        await session.commit()
        await session.refresh(tweet_model)
        return {
            "result": True,
            "tweet_id": tweet_model.id
        }

@router.post(path="/medias",)
async def tweet_media(file: UploadFile= File(...), api_key: str = Header(default=..., alias="api-key")):
    user_select = await session.execute(
        select(User)
        .where(User.api_key == api_key)
    )
    user = user_select.scalar()

    filelocation = f"./images/{file.filename}"
    async with aiofiles.open(filelocation, "wb") as outfile:
        content = await file.read()
        await outfile.write(content)
    media_model = Media(path_file=f"{filelocation}", user_id=user.id)
    session.add(media_model)
    await session.commit()
    await session.refresh(media_model)

    return {
        "result": True,
        "media_id": media_model.id
    }


@router.delete(path="/tweets/{id_tweet}",)
async def tweet_delete(id_tweet, api_key: str = Header(default=..., alias="api-key")):

    user_select = await session.execute(select(User).where(User.api_key == api_key))
    user = user_select.scalar()
    tweet_delete =await session.execute(select(Tweet).where(Tweet.id == int(id_tweet), Tweet.user_id == user.id))
    tweet_to_delete = tweet_delete.scalar()
    await session.delete(tweet_to_delete)
    await session.commit()
    return {"result": True}


@router.post(path="/tweets/{id_tweet}/likes",)
async def tweet_like(id_tweet, api_key: str = Header(default=..., alias="api-key")):
    user_select = await session.execute(
        select(User)
        .where(User.api_key == api_key)
    )
    user = user_select.scalar()
    like_model = Like(tweet_id=int(id_tweet),user_id=user.id)

    session.add(like_model)
    await session.commit()
    await session.refresh(like_model)
    return {"result": True}

@router.delete(path="/tweets/{id_tweet}/likes",)
async def tweet_unlike(id_tweet, api_key: str = Header(default=..., alias="api-key")):
    user_select = await session.execute(
        select(User)
        .where(User.api_key == api_key)
    )
    user = user_select.scalar()
    await session.execute(
        delete(Like)
        .where(Like.user_id == user.id, Like.tweet_id == int(id_tweet))
    )
    await session.commit()
    return {"result": True}

@router.post(path="/users/{id_user}/follow",)
async def tweet_follow(id_user, api_key: str = Header(default=..., alias="api-key")):
    user_select = await session.execute(select(User)
        .where(User.api_key == api_key))
    user = user_select.scalar()
    follow_model = Follow(follower_id=user.id, followed_id=int(id_user))
    session.add(follow_model)
    await session.commit()
    await session.refresh(follow_model)
    return {"result": True}

@router.delete(path="/users/{id_user}/follow",)
async def tweet_unfollow(id_user, api_key: str = Header(default=..., alias="api-key")):
    user_select = await session.execute(
        select(User)
        .where(User.api_key == api_key)
    )
    user = user_select.scalar()
    await session.execute(
        delete(Follow)
        .where(Follow.follower_id == user.id, Follow.followed_id == int(id_user))
    )
    await session.commit()
    return {"result": True}

@router.get(path="/tweets",)
async def tweet_get():

    res = await session.execute(select(Tweet))
    res = res.scalars().all()
    data = {
        "result": True,
        "tweets": [
           ]}

    for elem in res:
        likes = []
        like_d = await session.execute(select(Like).where(Like.tweet_id == elem.id))
        like_data = like_d.scalars()
        for like in like_data:
            name_user = await session.execute(select(User).where(User.id == like.user_id))
            name = name_user.scalar()
            likes.append({"user_id": like.user_id,
                        "name": name.name})
        attachments = []
        for file_id in elem.attachments:
            attachments_d = await session.execute(select(Media.path_file).where(Media.id == int(file_id)))
            attachments_data = attachments_d.scalar()
            attachments.append(attachments_data)
        data['tweets'].append( {
                "id": elem.id,
                "content": elem.content,
                "attachments": attachments,
                "author": {
                    "id": elem.user_id,
                    "name": elem.user.name,
                },
                "likes": likes
            })
    return data

@router.get(path="/users/{user_id}")
async def get_profile_for_id(user_id, api_key: str = Header(default=..., alias="api-key")):
    user_select = await session.execute(select(User).where(User.id == int(user_id)))
    result =  user_select.scalar()
    followers_d = await session.execute(select(Follow).where(Follow.followed_id == int(user_id)))
    followers_data = followers_d.scalars()
    followers_list = []
    for followers in followers_data:
        name_user = await session.execute(select(User).where(User.id == followers.follower_id))
        name = name_user.scalar()
        followers_list.append({"id": followers.follower_id,
                      "name": name.name})
    followed_d = await session.execute(select(Follow).where(Follow.follower_id == int(user_id)))
    followed_data = followed_d.scalars()
    followed_list = []
    for followed in followed_data:
        name_user = await session.execute(select(User).where(User.id == followed.followed_id))
        name = name_user.scalar()
        followed_list.append({"id": followed.followed_id,
                               "name": name.name})
    with open('sd.txt', 'a') as f:
        f.write(f"{followers_list} b {followed_list}")
    res = {
        "result": "true",
        "user": {
            "id": result.id,
            "name": result.name,
            "followers": followers_list,
            "following": followed_list
        }
    }
    return res