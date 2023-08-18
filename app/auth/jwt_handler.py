import time
from datetime import datetime

from fastapi import HTTPException, status
from jose import jwt, JWTError
from app.database.connection import get_setting

settings = get_setting()


def create_access_token(user: str):
    payload = {
        "user" : user,
        "expires" : time.time() + 3600
    }

    token = jwt.encode(payload, settings.secret_key, algorithm="HS256")
    return token


def verify_access_token(token: str):
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        expire = data.get("expires")

        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Acess Token supplied"
            )

        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired"
            )

        return data

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )