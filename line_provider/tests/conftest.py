import pytest
from httpx import AsyncClient

from interactors.in_memory_data_storage import DataStorage
from main import app


@pytest.fixture
async def async_client():
    """Fixture to initialize an AsyncClient for each test."""
    async with AsyncClient(base_url="http://localhost:8080/") as client:
        yield client


@pytest.fixture
async def app_connection():
    return app


@pytest.fixture
async def in_memory_data():
    return DataStorage().data