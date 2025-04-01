import time
import uuid

from adapters.publisher_pika_client import PikaPublisherClient
from fastapi import APIRouter, FastAPI, HTTPException
from interactors.in_memory_data_storage import DataStorage
from pydantic import UUID4
from schemas.event_schemas import (CreateEventSchema, EventListSchema,
                                   ResponseEventSchema, UpdateEventSchema)
from starlette import status

app = FastAPI()
data_storage = DataStorage()
router = APIRouter(prefix="/events")


@router.post("/events/", status_code=status.HTTP_201_CREATED)
async def create_event(request: CreateEventSchema) -> ResponseEventSchema:
    event_id = uuid.uuid4()
    data_storage.data[event_id] = request.model_dump()
    pika_client = PikaPublisherClient()
    message = ResponseEventSchema(id=event_id, **data_storage.data[event_id])
    await pika_client.publish_to_queue(message)
    return message


@router.get("/events/", status_code=status.HTTP_200_OK)
async def get_events() -> EventListSchema:
    return EventListSchema(
        events={event_id: event for event_id, event in data_storage.data.items() if time.time() < event.deadline}
    )


@router.get("/events/{event_id}", status_code=status.HTTP_200_OK)
async def get_event(event_id: UUID4) -> ResponseEventSchema:
    try:
        return ResponseEventSchema(id=event_id, **data_storage.data[event_id])
    except KeyError:
        raise HTTPException(status_code=404, detail="Event not found")


@router.put("/events/{event_id}", status_code=status.HTTP_200_OK)
async def update_event(event_id: UUID4, update_data: CreateEventSchema) -> ResponseEventSchema:
    if event_id in data_storage.data:
        data_storage.data[event_id] = update_data.model_dump()
        return ResponseEventSchema(id=event_id, **data_storage.data[event_id])
    else:
        raise HTTPException(status_code=404, detail="Event not found")


@router.patch("/events/{event_id}", status_code=status.HTTP_200_OK)
async def partially_update_event(event_id: UUID4, update_data: UpdateEventSchema) -> ResponseEventSchema:
    if event_id in data_storage.data:
        existing_data = data_storage.data[event_id]
        existing_data.update(update_data.model_dump(exclude_none=True))
        data_storage.data[event_id] = existing_data
        return ResponseEventSchema(id=event_id, **data_storage.data[event_id])
    else:
        raise HTTPException(status_code=404, detail="Event not found")


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: UUID4) -> None:
    if event_id in data_storage.data:
        data_storage.data.pop(event_id)
    else:
        raise HTTPException(status_code=404, detail="Event not found")
