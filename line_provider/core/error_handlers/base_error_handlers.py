from core.errors.base_error import BaseError
from core.schemas.base_error_schemas import (ErrorResponse,
                                             MultipleErrorResponse)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


def custom_base_errors_handler(_: Request, error: BaseError) -> JSONResponse:
    """This function is called if the BaseError was raised."""

    response = ErrorResponse(detail=error.detail, message=error.message)

    return JSONResponse(
        response.model_dump(by_alias=True),
        status_code=error.status_code,
    )


def pydantic_validation_errors_handler(
    _: Request,
    error: RequestValidationError,
) -> JSONResponse:
    """This function is called if the Pydantic validation error was raised."""

    response = MultipleErrorResponse(
        errors=[ErrorResponse(message=list(err["loc"]), detail=err["msg"]) for err in error.errors()]
    )

    return JSONResponse(
        content=jsonable_encoder(response.model_dump(by_alias=True)),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
