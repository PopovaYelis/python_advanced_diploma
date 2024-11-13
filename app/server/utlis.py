"""Utilities for routes."""

from database import session
from routes import Follow, Like, Media, Tweet, User
from schemas import UserOutSchema
from sqlalchemy import func
from sqlalchemy.future import select


async def get_users_info(user_id, user_name):
    """
    Get info about user by ID.

    Parameters:
        user_id (int): ID of the user,
        user_name (str): Name of the user.

    Returns:
        UserOutSchema: Info about the user.
    """
    followers_data = await session.execute(
        select(Follow).where(Follow.followed_id == int(user_id)),
    )
    follow_list = [[], []]
    for followers in followers_data.scalars():
        name_user = await session.execute(
            select(User).where(User.id == followers.follower_id),
        )
        follow_list[0].append({
            'id': followers.follower_id,
            'name': name_user.scalar().name,
        })

    followers_data = await session.execute(
        select(Follow).where(Follow.follower_id == int(user_id)),
    )
    for followed in followers_data.scalars():
        name_user = await session.execute(
            select(User).where(User.id == followed.followed_id),
        )
        follow_list[1].append({
            'id': followed.followed_id,
            'name': name_user.scalar().name,
        })

    return UserOutSchema(
        id=user_id,
        name=user_name,
        followers=follow_list[0],
        following=follow_list[1],
    )


async def get_user(api_key):
    """
    Get user by API key.

    Parameters:
        api_key (str): The API key used to identify the user.

    Returns:
        User: The user associated with the API key.
    """
    user_select = await session.execute(
        select(User).where(User.api_key == api_key),
    )
    return user_select.scalar()


async def get_tweets(id_f):
    """
    Get tweets by id_f key.

    Parameters:
        id_f (int): The id_f k used to identify the user.

    Returns:
        User: The user associated with the API key.
    """
    follower_count = await session.execute(
        select(func.count()).select_from(Follow).where(Follow.followed_id == id_f),
    )
    follower_count = follower_count.scalar()
    tweet_select = await session.execute(
        select(Tweet).where(Tweet.user_id == id_f),
    )

    return tweet_select.scalars(), follower_count


async def get_tweets_info(tweets_users):
    """
    Get tweets by id_f key.

    Parameters:
        tweets_users (list): The id_f k used to identify the user.

    Returns:
        User: The user associated with the API key.
    """
    data_tweets = []
    for elem in tweets_users[0]:
        likes = []
        like_d = await session.execute(
            select(Like).where(Like.tweet_id == elem.id),
        )
        for like in like_d.scalars():
            name_user = await session.execute(
                select(User).where(User.id == like.user_id),
            )
            likes.append({
                'user_id': like.user_id,
                'name': name_user.scalar().name,
            })
        attachments = []
        for file_id in elem.attachments:
            attachments_d = await session.execute(
                select(Media.path_file).where(Media.id == int(file_id)),
            )
            attachments.append(attachments_d.scalar())
        data_tweets.append({
            'id': elem.id,
            'content': elem.content,
            'attachments': attachments,
            'author': {
                'id': elem.user_id,
                'name': elem.user.name,
            },
            'likes': likes,
        },
        )

    return data_tweets
