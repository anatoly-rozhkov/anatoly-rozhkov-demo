from core.error_handlers.base_error_handlers import (
    custom_base_errors_handler, pydantic_validation_errors_handler)
from core.errors.base_error import BaseError
from core.settings import settings
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from routers.main_router import main_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="Bet Maker App")
origins = tuple([domain for domain in settings.cors_origins.split(" ")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=("*",),
    allow_headers=("*",),
)
app.include_router(main_router)
app.exception_handler(BaseError)(custom_base_errors_handler)
app.exception_handler(RequestValidationError)(pydantic_validation_errors_handler)
