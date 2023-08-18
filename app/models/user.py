from typing import List

from pydantic import BaseModel
from pydantic import ConfigDict
from sqlalchemy import Column, Integer, VARCHAR, JSON
from dataclasses import dataclass

from app.database.connection import Base


# from sqlmodel import SQLModel, Field, Column, JSON
#
#
# class User(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     email: EmailStr
#     password: str
#     events: Optional[List[Event]] = Field(sa_column=Column(JSON))
#
#     class Config:
#         schema_extra = {
#             "example" : {
#                 "email" : "...@...net",
#                 "username" : "kasd",
#                 "events" : []
#             }
#         }
#
#
# class UserSignIn(BaseModel):
#     email: EmailStr
#     password: str
#
#     class Config:
#         schema_extra = {
#             "example" : {
#                 "email" : "...@...net",
#                 "password" : "kasd",
#                 "events" : []
#             }
#         }


class User(Base):
    __tablename__ = 'user'

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int = Column('id', Integer, primary_key=True)
    email: str = Column('email', VARCHAR(255))
    password: str = Column('password', VARCHAR(255))
    username: str = Column('username', VARCHAR(255), nullable=False)
    events: List[str] = Column('events', JSON, nullable=True)


@dataclass
class UserSignUpModel(BaseModel):
    email: str
    password: str
    username: str


@dataclass
class UserSignInModel(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str