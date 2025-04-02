import decimal
import enum
from decimal import Decimal
from typing import Dict, Optional, Union

from pydantic import UUID4, BaseModel, Field
from schemas.base_schemas import BaseSchema


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class CreateEventSchema(BaseSchema):
    coefficient: decimal.Decimal = Field(..., description="Coefficient", ge=Decimal("1.01"))
    deadline: decimal.Decimal = Field(..., description="Deadline in seconds", ge=Decimal("30.00"))
    state: EventState = Field(..., description="Event state")


class UpdateEventSchema(BaseSchema):
    coefficient: Optional[decimal.Decimal] = Field(None, description="Coefficient", ge=Decimal("1.01"))
    deadline: Optional[decimal.Decimal] = Field(None, description="Deadline in seconds", ge=Decimal("30.00"))
    state: Optional[EventState] = Field(None, description="Event state")


class ResponseEventSchema(CreateEventSchema):
    id: Union[UUID4, str] = Field(description="Event ID")


class EventListSchema(BaseModel):
    events: Dict[Union[UUID4, str], CreateEventSchema]
