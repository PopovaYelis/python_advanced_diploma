from fastapi import APIRouter, Header, UploadFile, File
from sqlalchemy import delete
import aiofiles
from database import session, get_session
from models import User, Tweet, Like, Follow, Media
from sqlalchemy.future import select
from schemas import TweetSchema
from utlis import get_user, get_users_info

router = APIRouter()


@router.get(path="/users/me")
async def get_profile_my(api_key: str = Header(default=..., alias="api-key")):
    result = await get_user(api_key)
    user_model = await get_users_info(result.id, result.name)
    res = {
        "result": True,
        "user":
            user_model.model_dump()
    }

    return res


@router.post(path="/tweets")
async def tweet_post(tweet_data: TweetSchema, api_key: str = Header(default=..., alias="api-key")):
    user = await get_user(api_key)
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
    user = await get_user(api_key)
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
    user = await get_user(api_key)
    tweet_delete =await session.execute(select(Tweet).where(Tweet.id == int(id_tweet), Tweet.user_id == user.id))
    tweet_to_delete = tweet_delete.scalar()
    await session.delete(tweet_to_delete)
    await session.commit()
    return {"result": True}


@router.post(path="/tweets/{id_tweet}/likes",)
async def tweet_like(id_tweet, api_key: str = Header(default=..., alias="api-key")):
    user = await get_user(api_key)
    like_model = Like(tweet_id=int(id_tweet),user_id=user.id)

    session.add(like_model)
    await session.commit()
    await session.refresh(like_model)
    return {"result": True}

@router.delete(path="/tweets/{id_tweet}/likes",)
async def tweet_unlike(id_tweet, api_key: str = Header(default=..., alias="api-key")):
    user = await get_user(api_key)
    await session.execute(
        delete(Like)
        .where(Like.user_id == user.id, Like.tweet_id == int(id_tweet))
    )
    await session.commit()
    return {"result": True}

@router.post(path="/users/{id_user}/follow",)
async def tweet_follow(id_user, api_key: str = Header(default=..., alias="api-key")):
    user = await get_user(api_key)
    follow_model = Follow(follower_id=user.id, followed_id=int(id_user))
    session.add(follow_model)
    await session.commit()
    await session.refresh(follow_model)
    return {"result": True}

@router.delete(path="/users/{id_user}/follow",)
async def tweet_unfollow(id_user, api_key: str = Header(default=..., alias="api-key")):
    user = await get_user(api_key)
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
    user_model = await get_users_info(user_id, user_select.scalar().name)
    res = {
        "result": True,
        "user": user_model.model_dump()
    }
    return res

