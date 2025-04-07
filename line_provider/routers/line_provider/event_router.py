import time
import uuid
from datetime import datetime, timezone
from decimal import ROUND_UP, Decimal
from typing import Union

from adapters.publisher_pika_client import PikaPublisherClient
from fastapi import APIRouter, FastAPI, HTTPException
from interactors.in_memory_data_storage import DataStorage
from pydantic import UUID4, ValidationError
from schemas.event_schemas import (CreateEventSchema, EventListSchema,
                                   EventResponseSchema, UpdateEventSchema)
from starlette import status

app = FastAPI()
data_storage = DataStorage()
router = APIRouter(prefix="")


@router.post("/events/", status_code=status.HTTP_201_CREATED)
async def create_event(request: CreateEventSchema) -> EventResponseSchema:
    event_id = str(uuid.uuid4())

    data = request.model_dump()
    data["deadline"] = Decimal(str(time.time())).quantize(Decimal("0.01"), rounding=ROUND_UP) + data["deadline"]
    data["created_at"] = datetime.now(timezone.utc)
    data_storage.data[event_id] = data

    pika_client = PikaPublisherClient()
    await pika_client.publish_to_queue(dict(data_storage.data[event_id], id=event_id))

    return EventResponseSchema(id=event_id, **data_storage.data[event_id])


@router.get("/events/", status_code=status.HTTP_200_OK)
async def get_events() -> EventListSchema:
    return EventListSchema(
        results={event_id: event for event_id, event in data_storage.data.items() if time.time() < event["deadline"]}
    )


@router.get("/events/{event_id}", status_code=status.HTTP_200_OK)
async def get_event(event_id: Union[UUID4, str]) -> EventResponseSchema:
    try:
        return EventResponseSchema(id=event_id, **data_storage.data[str(event_id)])
    except KeyError:
        raise HTTPException(status_code=404, detail="Event not found")
    except ValidationError:
        raise HTTPException(status_code=422, detail="Invalid data format")


@router.put("/events/{event_id}", status_code=status.HTTP_200_OK)
async def update_event(event_id: Union[UUID4, str], update_data: CreateEventSchema) -> EventResponseSchema:
    event_id = str(event_id)
    if event_id in data_storage.data:
        created_at = data_storage.data[event_id]["created_at"]

        data = update_data.model_dump()
        data["updated_at"] = datetime.now(timezone.utc)
        data["created_at"] = created_at

        data_storage.data[event_id] = data

        pika_client = PikaPublisherClient()
        await pika_client.publish_to_queue(dict(data_storage.data[event_id], id=event_id))
        try:
            return EventResponseSchema(id=event_id, **data_storage.data[event_id])
        except ValidationError:
            raise HTTPException(status_code=422, detail="Invalid data format")
    else:
        raise HTTPException(status_code=404, detail="Event not found")


@router.patch("/events/{event_id}", status_code=status.HTTP_200_OK)
async def partially_update_event(event_id: Union[UUID4, str], update_data: UpdateEventSchema) -> EventResponseSchema:
    event_id = str(event_id)
    if event_id in data_storage.data:
        existing_data = data_storage.data[event_id]
        existing_data.update(update_data.model_dump(exclude_none=True))
        existing_data["updated_at"] = datetime.now(timezone.utc)
        data_storage.data[event_id] = existing_data

        pika_client = PikaPublisherClient()
        await pika_client.publish_to_queue(dict(data_storage.data[event_id], id=event_id))
        try:
            return EventResponseSchema(id=event_id, **data_storage.data[event_id])
        except ValidationError:
            raise HTTPException(status_code=422, detail="Invalid data format")
    else:
        raise HTTPException(status_code=404, detail="Event not found")


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: Union[UUID4, str]) -> None:
    event_id = str(event_id)
    if event_id in data_storage.data:
        data_storage.data.pop(event_id)
    else:
        raise HTTPException(status_code=404, detail="Event not found")
