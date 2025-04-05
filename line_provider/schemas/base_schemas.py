from datetime import datetime
from typing import Optional, Union

from pydantic import UUID4, BaseModel, Field


class BaseSchema(BaseModel):
    class Config:
        """
        Schema config.
        """

        from_attributes = True


class BaseResponseSchema:
    created_at: datetime = Field(..., description="Created At")
    updated_at: Optional[datetime] = Field(None, description="Updated At")
