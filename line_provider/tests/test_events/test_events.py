import time
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient
from interactors.in_memory_data_storage import DataStorage
from main import app


@patch("adapters.publisher_pika_client.PikaPublisherClient.publish_to_queue", mock_rabbit=AsyncMock)
@pytest.mark.asyncio
async def test_simple_workflow(mock_rabbit):
    data_storage = DataStorage()

    test_id = str(uuid.uuid4())

    data_storage.data[test_id] = {
        "name": "test",
        "coefficient": 1.1,
        "deadline": int(time.time()) + 600,
        "state": 1,
        "created_at": str(datetime.now(timezone.utc)),
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as ac:
        create_response = await ac.put(f"/api/events/{test_id}", json=data_storage.data[test_id])

    a = create_response
    assert create_response.status_code == 200

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as ac:
        response = await ac.get(f"/api/events/{test_id}")

    assert response.status_code == 200

    updated_event = data_storage.data[test_id].copy()
    updated_event["state"] = 2

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as ac:
        update_response = await ac.patch(f"/api/events/{test_id}", json={"event_id": test_id, "state": 2})

    assert update_response.status_code == 200

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as ac:
        response = await ac.get(f"/api/events/{test_id}")

    assert response.status_code == 200
