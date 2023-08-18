import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.tests.confest import test_session
from app.routes.events import event_router
from app.auth.jwt_handler import create_access_token
from app.models.events import Event

app = FastAPI()
app.include_router(event_router, prefix="/event")

# 앱 라우터 및 설정 등 추가

client = TestClient(app)



def access_token() -> str:
    return create_access_token("testuser@packt.com")


@pytest.mark.asyncio
async def test_post_event(test_session) -> None:
    payload = {
        "title" : "FastAPI Book Launch",
        "image" : "https://linktomyimage.com/image.png",
        "description" : "We will be discussing the contents of the Fast api..",
        "tags" : ["python", "fastapi", "book"],
        "location" : "google meet"
    }

    headers = {
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {access_token()}"
    }

    test_response = {
        "message" : "Event created successfully"
    }

    response = client.post("/event", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_get_event(test_session) -> None:

    headers = {
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {access_token()}"
    }

    response_body = {
        "title": "FastAPI Book Launch",
        "image": "https://linktomyimage.com/image.png",
        "description": "We will be discussing the contents of the Fast api..",
        "tags": ["python", "fastapi", "book"],
        "location": "google meet"
    }

    response = client.get("/event/5")

    assert response.status_code == 200
    assert response.json() == response_body