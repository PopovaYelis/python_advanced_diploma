"""Schemas for api."""

import aiofiles
from database import session
from fastapi import APIRouter, File, Header, UploadFile
from models import Follow, Like, Media, Tweet, User
from schemas import TweetSchema
from sqlalchemy import delete
from sqlalchemy.future import select
from utlis import get_tweets, get_tweets_info, get_user, get_users_info

router = APIRouter()


@router.get(path='/users/me')
async def get_profile_my(api_key: str = Header(default=..., alias='api-key')):
    """
    Get information about me.

    Parameters:
        api_key (str): The API key used to identify the user.

    Returns:
        dict: Information about me.
    """
    result_user = await get_user(api_key)
    user_model = await get_users_info(result_user.id, result_user.name)
    return {
        'result': True,
        'user': user_model.model_dump(),
    }


@router.post(path='/tweets')
async def tweet_post(tweet_data: TweetSchema, api_key: str = Header(default=..., alias='api-key')):
    """
    Add post.

    Parameters:
        tweet_data (TweetSchema): tweet content
        api_key (str): The API key used to identify the user.

    Returns:
        dict: Information about success.
    """
    user = await get_user(api_key)
    if user:
        user_id = user.id
        tweet_model = Tweet(content=tweet_data.tweet_data, attachments=tweet_data.tweet_media_ids, user_id = user_id)
        session.add(tweet_model)
        await session.commit()
        await session.refresh(tweet_model)
        return {
            'result': True,
            'tweet_id': tweet_model.id,
        }


@router.post(path='/medias')
async def tweet_media(file_media: UploadFile = File(...), api_key: str = Header(default=..., alias='api-key')):
    """
    Add media.

    Parameters:
        file_media (UploadFile): file media
        api_key (str): The API key used to identify the user.

    Returns:
        dict: Information about success.
    """
    user = await get_user(api_key)
    filelocation = './images/{file}'.format(file=file_media.filename)
    async with aiofiles.open(filelocation, 'wb') as outfile:
        content_media = await file_media.read()
        await outfile.write(content_media)
    media_model = Media(path_file=filelocation, user_id=user.id)
    session.add(media_model)
    await session.commit()
    await session.refresh(media_model)

    return {
        'result': True,
        'media_id': media_model.id,
    }


@router.delete(path='/tweets/{id_tweet}')
async def tweet_delete(id_tweet, api_key: str = Header(default=..., alias='api-key')):
    """
    Delete tweet by id.

    Parameters:
        id_tweet (int): id Tweet
        api_key (str): The API key used to identify the user.

    Returns:
        dict: Information about success.
    """
    user = await get_user(api_key)
    tweet_deleting = await session.execute(select(Tweet).where(
        Tweet.id == int(id_tweet), Tweet.user_id == user.id,
    ),
    )
    tweet_to_delete = tweet_deleting.scalar()
    await session.delete(tweet_to_delete)
    await session.commit()
    return {'result': True}


@router.post(path='/tweets/{id_tweet}/likes')
async def tweet_like(id_tweet, api_key: str = Header(default=..., alias='api-key')):
    """
    Like tweet by id.

    Parameters:
        id_tweet (int): id Tweet
        api_key (str): The API key used to identify the user.

    Returns:
        dict: Information about success.
    """
    user = await get_user(api_key)
    like_model = Like(tweet_id=int(id_tweet), user_id=user.id)
    session.add(like_model)
    await session.commit()
    await session.refresh(like_model)
    return {'result': True}


@router.delete(path='/tweets/{id_tweet}/likes')
async def tweet_unlike(id_tweet, api_key: str = Header(default=..., alias='api-key')):
    """
    Unlike tweet by id.

    Parameters:
        id_tweet (int): id Tweet
        api_key (str): The API key used to identify the user.

    Returns:
        dict: Information about success.
    """
    user = await get_user(api_key)
    await session.execute(
        delete(Like).where(
            Like.user_id == user.id, Like.tweet_id == int(id_tweet),
        ),
    )
    await session.commit()
    return {'result': True}


@router.post(path='/users/{id_user}/follow')
async def tweet_follow(id_user, api_key: str = Header(default=..., alias='api-key')):
    """
    Follow user by id.

    Parameters:
        id_user (int): id User
        api_key (str): The API key used to identify the user.

    Returns:
        dict: Information about success.
    """
    user = await get_user(api_key)
    follow_model = Follow(follower_id=user.id, followed_id=int(id_user))
    session.add(follow_model)
    await session.commit()
    await session.refresh(follow_model)
    return {'result': True}


@router.delete(path='/users/{id_user}/follow')
async def tweet_unfollow(id_user, api_key: str = Header(default=..., alias='api-key')):
    """
    Unfollow user by id.

    Parameters:
        id_user (int): id User
        api_key (str): The API key used to identify the user.

    Returns:
        dict: Information about success.
    """
    user = await get_user(api_key)
    await session.execute(
        delete(Follow).where(
            Follow.follower_id == user.id, Follow.followed_id == int(id_user),
        ),
    )
    await session.commit()
    return {'result': True}


@router.get(path='/tweets')
async def tweet_get() -> dict:
    """
    Get tweets information by user api_key.

    Returns:
        dict: A dictionary containing the info about the tweets.
    """
    user = await session.execute(select(User))
    users_ids = [user.id for user in user.scalars()]
    tweets = []
    for id_f in users_ids:
        data_d = await get_tweets(id_f)
        tweets.append(data_d)
    data_tweets = {
        'result': True,
        'tweets': [
        ],
    }
    tweets.sort(key=lambda x_1: x_1[1], reverse=True)
    for tweets_users in tweets:
        data_tweets['tweets'].extend(await get_tweets_info(tweets_users))
    return data_tweets


@router.get(path='/users/{user_id}')
async def get_profile_for_id(user_id):
    """
    Get user profile information by user ID.

    Parameters:
        user_id (int): ID of the user,

    Returns:
        dict: Info about the user.
    """
    user_select = await session.execute(
        select(User).where(User.id == int(user_id)),
    )
    user_model = await get_users_info(user_id, user_select.scalar().name)
    return {
        'result': True,
        'user': user_model.model_dump(),
    }
