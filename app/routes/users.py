from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from app.models.user import User, UserSignInModel, TokenResponse, UserSignUpModel
from sqlalchemy import select
from app.database.connection import get_session, session
from app.auth.hash_password import HashPassword
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt_handler import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(tags=["user"])
hash_password = HashPassword()


@user_router.post("/signup")
async def sign_new_user(request_user: UserSignUpModel,
                        session:AsyncSession = Depends(get_session)) -> dict:

    user = await session.execute(select(User).where(User.email == request_user.email))

    if user.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    hashed_password = hash_password.created_hash(request_user.password)
    request_user.password = hashed_password
    new_user: User = User(**request_user.model_dump())
    session.add(new_user)

    return {
        "message": "User created successfully"
    }


@user_router.post("/signin", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def sign_user_in(request_user: UserSignInModel,
                       session: AsyncSession = Depends(get_session)
                       ) -> JSONResponse:

    user_exist_req = await session.execute(select(User).filter(User.email == request_user.email))

    user_exist = user_exist_req.scalar()

    if hash_password.verify_hash(request_user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return JSONResponse(
            content={"access_token": access_token, "token_type": "Bearer"},
            headers={"Authorization": "Bearer "+access_token}
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Invalid details passed"
    )