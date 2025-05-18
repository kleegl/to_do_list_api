from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from basic_auth import get_password_hash, verify_credentials
from core import get_db
from models import User
from request import UserCreateRequest, UserUpdateRequest
from response import UserBaseResponse, UserResponse


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user(user: UserBaseResponse = Depends(verify_credentials)):
    return user


@user_router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_by_id(
    id: int,
    session: AsyncSession = Depends(get_db),
    # username: str = Depends(verify_credentials),
):
    user_from_db = await session.get(User, id, options=[selectinload(User.tasks)])
    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id = {id} not found",
        )
    return user_from_db


@user_router.post(
    "/create", response_model=UserBaseResponse, status_code=status.HTTP_201_CREATED
)
async def create(
    create_user: UserCreateRequest, session: AsyncSession = Depends(get_db)
):
    try:
        user = User(
            name=create_user.name,
            password_hash=get_password_hash(create_user.password),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    return user


@user_router.patch(
    "/update", response_model=UserBaseResponse, status_code=status.HTTP_200_OK
)
async def update(
    update_user: UserUpdateRequest,
    session: AsyncSession = Depends(get_db),
    current_user: UserBaseResponse = Depends(verify_credentials),
):
    try:
        user = await session.get(User, current_user.id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id = {current_user.id} not found",
            )

        if update_user.name:
            user.name = update_user.name
        if update_user.password:
            user.password_hash = update_user.password

        await session.commit()
        await session.refresh(user)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    return user


@user_router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, session: AsyncSession = Depends(get_db)):
    try:
        user = await session.get(User, id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id = {id} not found",
            )
        await session.delete(user)
        await session.commit()
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
