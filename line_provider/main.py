from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.settings import settings
from routers.main_router import main_router

app = FastAPI(title="Line Provider App")
origins = tuple([domain for domain in settings.cors_origins.split(" ")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=("*",),
    allow_headers=("*",),
)
app.include_router(main_router)