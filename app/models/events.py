from app.database.connection import Base
from sqlalchemy import Column, Integer, VARCHAR, JSON
from typing import List
from dataclasses import dataclass
from typing import Union
from pydantic import ConfigDict, BaseModel

# class Event(BaseModel):
#     id: int
#     title: str
#     image: str
#     description: str
#     tags: List[str]
#     location: str
#
#     class Config:
#         json_schema_extra = {
#             "example" : {
#                 "title" : "name",
#                 "image": "...png",
#                 "description": "desc",
#                 "tags": ["python","fastapi"],
#                 "location": "google office",
#             }
#         }

# class Event(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     title: str
#     image: str
#     description: str
#     tags: List[str] = Field(sa_column=Column(JSON))
#     location: str
#     creator: Optional[str]
#
#     class Config:
#         arbitrary_types_allowed = True
#         schema_extra = {
#             "example" : {
#                 "title" : "name",
#                 "image": "...png",
#                 "description": "desc",
#                 "tags": ["python","fastapi"],
#                 "location": "google office",
#             }
#         }
#
#
# class EventUpdate(BaseModel):
#
#     title: Optional[str] = None
#     image: Optional[str] = None
#     description: Optional[str] = None
#     tags: Optional[List[str]] = Field(sa_column=Column(JSON))
#     location: Optional[str] = None
#
#     class Config:
#         arbitrary_types_allowed = True
#         schema_extra = {
#             "example" : {
#                 "title" : "name",
#                 "image": "...png",
#                 "description": "desc",
#                 "tags": ["python","fastapi"],
#                 "location": "google office",
#             }
#         }


class Event(Base):
    __tablename__ = 'event'

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int = Column('id', Integer, primary_key=True)
    title: str = Column('title', VARCHAR(255))
    image: str = Column('image', VARCHAR(255))
    description: str = Column('description', VARCHAR(255))
    tags: List[str] = Column('tags', JSON, nullable=True)
    location: str = Column('location', VARCHAR(255))


@dataclass
class EventModel(BaseModel):

    title: str
    image: Union[str, None]
    description: Union[str, None]
    tags: Union[List[str], None]
    location: Union[str, None]

class EventResposne(BaseModel):
    id: int
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Config:
        orm_mode = True