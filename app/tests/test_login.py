import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.tests.confest import test_session
from app.routes.users import user_router
from app.models.user import User
from sqlalchemy import MetaData

app = FastAPI()
app.include_router(user_router, prefix="/user")

# 앱 라우터 및 설정 등 추가

client = TestClient(app)


@pytest.fixture(scope="session")
async def remove_all_user(test_session) -> None:
    MetaData.remove(User)



@pytest.mark.asyncio
async def test_sign_new_user(test_session) -> None:

    payload = {
        "email": "test6@packt.com",
        "username": "231",
        "password": "123"
    }
    headers = {
        "accept" : "application/json",
        "Content-Type" : "application/json"
    }
    test_response = {
        "message" : "User created successfully"
    }
    response = client.post("/user/signup", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_signin_success(test_session) -> None:
    ##given
    payload = {
        "email": "test6@packt.com",
        "password": "123"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    response = client.post("/user/signin", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"



# @pytest.mark.asyncio
# async def test_signin_fail(test_session) -> None:
#     ##given
#     payload = {
#         "email": "2321asd@packt.com",
#         "password": "asd"
#     }
#     headers = {
#         "accept": "application/json",
#         "Content-Type": "application/json"
#     }
#     response = client.post("/user/signin", json=payload, headers=headers)
#     assert response.status_code == 401
#     assert response.json()["token_type"] == "Bearer"