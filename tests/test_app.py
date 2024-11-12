from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.server.models import User


async def test_route_user_me(client, session):
    async with session:
        res = await session.execute(select(User).where(User.id == 1))

    get_user: User | None = res.scalar()
    api_key: str | None = get_user.api_key
    response = await client.get(
        "http://testhost/api/users/me", headers={"api-key": api_key}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True

async def test_route_user_id(client, session):
    async with session:
        res = await session.execute(select(User).where(User.id == 1))

    get_user: User | None = res.scalar()
    api_key: str | None = get_user.api_key
    response = await client.get(
        "http://testhost/api/users/1", headers={"api-key": api_key}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True

async def test_route_follow(client, session):
    async with session:
        res = await session.execute(select(User).where(User.id == 1))

    get_user: User | None = res.scalar()
    api_key: str | None = get_user.api_key
    response = await client.post(
        "http://testhost/api/users/2/follow", headers={"api-key": api_key}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True

async def test_route_unfollow(client, session):
    async with session:
        res = await session.execute(select(User).where(User.id == 1))

    get_user: User | None = res.scalar()
    api_key: str | None = get_user.api_key
    response = await client.delete(
        "http://testhost/api/users/2/follow", headers={"api-key": api_key}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True


async def test_route_tweet_post(session: AsyncSession, client: AsyncClient) -> None:
    async with session:
        get_user_select = await session.execute(select(User).where(User.id == 1))
    get_user: User | None = get_user_select.scalar()
    api_key: str | None = get_user.api_key

    new_tweet = {
        "tweet_data": "test tweet 1",
        "tweet_media_ids": []
    }
    response = await client.post(
        "http://testhost/api/tweets",
        headers={"api-key": api_key},
        json=new_tweet,
    )

    assert response.status_code == 200
    assert response.json()["result"] is True

async def test_route_tweet_get(session: AsyncSession, client: AsyncClient) -> None:
    async with session:
        get_user_select = await session.execute(select(User).where(User.id == 1))
    get_user: User | None = get_user_select.scalar()
    api_key: str | None = get_user.api_key

    response = await client.get(
        "http://testhost/api/tweets",
        headers={"api-key": api_key},
    )

    assert response.status_code == 200
    assert response.json()["result"] is True

async def test_route_tweet_like(session: AsyncSession, client: AsyncClient) -> None:
    async with session:
        get_user_select = await session.execute(select(User).where(User.id == 1))
    get_user: User | None = get_user_select.scalar()
    api_key: str | None = get_user.api_key
    response = await client.post(
        "http://testhost/api/tweets/1/likes",
        headers={"api-key": api_key},
    )
    assert response.status_code == 200
    assert response.json()["result"] is True

async def test_route_tweet_dislike(session: AsyncSession, client: AsyncClient) -> None:
    async with session:
        get_user_select = await session.execute(select(User).where(User.id == 1))
    get_user: User | None = get_user_select.scalar()
    api_key: str | None = get_user.api_key
    response = await client.delete(
        "http://testhost/api/tweets/1/likes",
        headers={"api-key": api_key},
    )
    assert response.status_code == 200
    assert response.json()["result"] is True

async def test_route_tweet_delete(session: AsyncSession, client: AsyncClient) -> None:
    async with session:
        get_user_select = await session.execute(select(User).where(User.id == 1))
    get_user: User | None = get_user_select.scalar()
    api_key: str | None = get_user.api_key
    response = await client.delete(
        "http://testhost/api/tweets/1",
        headers={"api-key": api_key},
    )
    assert response.status_code == 200
    assert response.json()["result"] is True