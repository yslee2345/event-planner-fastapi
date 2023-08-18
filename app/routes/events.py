from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select, text
from app.database.connection import get_session

from app.auth.authenticate import authenticate
from app.database.connection import session
from app.models.events import Event, EventModel
from sqlalchemy.ext.asyncio import AsyncSession

event_router = APIRouter(
    tags=['Events']
)

events = []


@event_router.get("/{id}", response_model=EventModel, status_code=status.HTTP_200_OK)
async def retrieve_event(id: int,
                         session: AsyncSession = Depends(get_session)) -> EventModel:
    event = await session.execute(select(Event).where(Event.id == id))
    if event:
        return event.scalar_one()
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


# @event_router.post("/new")
# async def create_event(body: Event = Body(...)) -> dict:
#     events.append(body)
#     return {
#         "message" : "Event created successfully"
#     }

@event_router.post("/")
async def create_event(request_event:EventModel,
                       session:AsyncSession = Depends(get_session),
                       user: str = Depends(authenticate)) -> dict:
    new_event = Event(**request_event.model_dump())
    session.add(new_event)
    return {
        "message": "Event created successfully"
    }
#
#
# @event_router.delete("/{id}")
# async def delete_event(id: int,
#                        user: str = Depends(authenticate),
#                        session: AsyncSession = Depends(get_session)) -> dict:
#     event = session.get(entity=Event, ident=id)
#     if event:
#         session.delete(event)
#         session.commit()
#         return {
#             "message" : "Event deleted sucessfully."
#         }
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Event with supplied ID does not exist"
#     )
#
#
# @event_router.put("/{id}", response_model=None)
# async def update_event(id: int,
#                        body: Event,
#                        user: str = Depends(authenticate),
#                        session:AsyncSession=Depends(get_session)) -> Event:
#     event = session.get(entity=Event, ident=id)
#     if event.creator != user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Operation not allowed"
#         )
#     statement = select(Event).where(Event.id == id)
#     exists_event = session.exec(statement).first()
#     if exists_event:
#         exists_event.title = body.title
#         session.add(exists_event)
#         session.commit()
#     return exists_event
