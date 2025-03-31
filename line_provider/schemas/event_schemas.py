import decimal
import enum
from typing import Dict, Optional, Union

from pydantic import UUID4, BaseModel, Field
from schemas.base_schemas import BaseSchema


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class CreateEventSchema(BaseSchema):
    coefficient: decimal.Decimal = Field(..., description="Coefficient")
    deadline: int = Field(..., description="Deadline in seconds")
    state: EventState = Field(..., description="Event state")


class UpdateEventSchema(BaseSchema):
    coefficient: Optional[decimal.Decimal] = Field(None, description="Coefficient")
    deadline: Optional[int] = Field(None, description="Deadline in seconds")
    state: Optional[EventState] = Field(None, description="Event state")


class ResponseEventSchema(CreateEventSchema):
    id: Union[UUID4, str] = Field(description="Event ID")


class EventListSchema(BaseModel):
    events: Dict[Union[UUID4, str], CreateEventSchema]
