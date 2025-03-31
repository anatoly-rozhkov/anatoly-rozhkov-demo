from pydantic import BaseModel, conlist


class ErrorResponse(BaseModel):
    message: str | list
    detail: str


class MultipleErrorResponse(BaseModel):
    errors: conlist(ErrorResponse, min_length=1)
