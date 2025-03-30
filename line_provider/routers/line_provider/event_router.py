import uuid

from fastapi import FastAPI, APIRouter, HTTPException
from starlette import status

from interactors.in_memory_data_storage import DataStorage
from schemas.event_schemas import ResponseEvent, RequestEvent

app = FastAPI()
data_storage = DataStorage()

router = APIRouter(prefix="/events")

@router.post("/events/", status_code=status.HTTP_201_CREATED)
async def create_event(request: RequestEvent) -> ResponseEvent:
    event_id = uuid.uuid4()
    data_storage.data[event_id] = request.model_dump()

    return ResponseEvent(id=event_id, **data_storage.data[event_id])

@router.get("/events/")
async def get_event():
    pass
    # if event:
    #     return event
    # else:
    #     raise HTTPException(status_code=404, detail="Event not found")
#
# @router.put("/events/{event_id}")
# async def update_event(event_id: UUID4, update_data: Event):
#     event = event_crud.update(event_id, update_data)
#     if event:
#         return event
#     else:
#         raise HTTPException(status_code=404, detail="Event not found")
#
# @router.delete("/events/{event_id}")
# async def delete_event(event_id: UUID4):
#     deleted_event = event_crud.delete(event_id)
#     if deleted_event:
#         return deleted_event
#     else:
#         raise HTTPException(status_code=404, detail="Event not found")
