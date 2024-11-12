from database import session
from routes import User, Follow
from sqlalchemy.future import select
from schemas import UserOutSchema


async def get_users_info(user_id, user_name):
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
    return UserOutSchema(id=user_id,name=user_name, followers=followers_list, following=followed_list)

async def get_user(api_key):
    user_select = await session.execute(select(User).where(User.api_key == api_key))
    result = user_select.scalar()
    return result
