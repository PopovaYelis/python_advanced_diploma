from pydoc import describe

from sqlalchemy import Column, String, Integer, ForeignKey, ARRAY
from sqlalchemy.orm import (
    DeclarativeBase,
    declarative_base,
    relationship,
)
from typing import Dict, Any
from database import Base, session

class User(Base):
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False, unique=True)
    api_key: str = Column(String, unique=True, index=True)
    tweets = relationship("Tweet", back_populates="user")
    likes = relationship("Like", back_populates="user")

    followers = relationship(
        "Follow",
        back_populates="followed",
        foreign_keys="[Follow.followed_id]",
        lazy="selectin",
    )
    following = relationship(
        "Follow",
        back_populates="follower",
        foreign_keys="[Follow.follower_id]",
        lazy="selectin",
    )

class Tweet(Base):
    __tablename__ = 'tweets'
    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    content: str = Column(String(280), nullable=False)
    attachments = Column(ARRAY(Integer))
    user = relationship("User", back_populates="tweets", lazy="joined")
    likes = relationship("Like", back_populates="tweet", lazy="select", cascade="all, delete-orphan")

class Like(Base):
    __tablename__ = "likes"

    tweet_id: int = Column(Integer, ForeignKey("tweets.id"), nullable=False, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False, primary_key=True)
    tweet = relationship("Tweet", back_populates="likes")
    user = relationship("User", back_populates="likes")

class Media(Base):
    __tablename__ = "medias"

    id: int = Column(Integer, primary_key=True)
    path_file: str = Column(String, nullable=False)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)


class Follow(Base):

    __tablename__ = "followers"

    follower_id: int = Column(Integer, ForeignKey("users.id"), primary_key=True)
    followed_id: int = Column(Integer, ForeignKey("users.id"), primary_key=True)
    follower = relationship("User", foreign_keys=[follower_id])
    followed = relationship("User", foreign_keys=[followed_id])




