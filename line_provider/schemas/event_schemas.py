from pydantic import UUID4, Field

from schemas.base_schemas import BaseSchema
import decimal
import enum
from typing import Optional


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class RequestEvent(BaseSchema):
    coefficient: Optional[decimal.Decimal] = Field(..., description="Coefficient")
    deadline: Optional[int] = Field(..., description="Deadline in seconds")
    state: Optional[EventState] = Field(..., description="Event state")


class ResponseEvent(RequestEvent):
    id: UUID4 = Field(description="Event ID")