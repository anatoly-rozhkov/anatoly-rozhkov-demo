import decimal
from decimal import Decimal
from typing import Dict, Optional, Union

from enums.event_enums import EventState
from pydantic import UUID4, BaseModel, Field
from schemas.base_schemas import BaseResponseSchema, BaseSchema


class CreateEventSchema(BaseSchema):
    name: str = Field(..., description="Name")
    coefficient: decimal.Decimal = Field(..., description="Coefficient", ge=Decimal("1.01"))
    deadline: decimal.Decimal = Field(..., description="Deadline in seconds", ge=Decimal("30.00"))
    state: EventState = Field(..., description="Event state")


class UpdateEventSchema(BaseSchema):
    name: Optional[str] = Field(None, description="Name")
    coefficient: Optional[decimal.Decimal] = Field(None, description="Coefficient", ge=Decimal("1.01"))
    deadline: Optional[decimal.Decimal] = Field(None, description="Deadline in seconds", ge=Decimal("30.00"))
    state: Optional[EventState] = Field(None, description="Event state")


class EventResponseSchema(BaseResponseSchema, CreateEventSchema):
    id: Union[UUID4, str] = Field(..., description="ID")


class SingleEventSchema(CreateEventSchema, BaseResponseSchema):
    pass


class EventListSchema(BaseModel):
    results: Dict[Union[UUID4, str], SingleEventSchema]
