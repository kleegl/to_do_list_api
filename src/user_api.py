from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from core import get_db
from models import User
from request import UserCreateRequest, UserUpdateRequest
from response import UserBaseResponse, UserResponse


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_by_id(id: int, session: AsyncSession = Depends(get_db)):
    user_from_db = await session.get(User, id, options=[selectinload(User.tasks)])
    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id = {id} not found",
        )
    return user_from_db


@user_router.post(
    "/create", response_model=UserBaseResponse, status_code=status.HTTP_200_OK
)
async def create(
    create_user: UserCreateRequest, session: AsyncSession = Depends(get_db)
):
    try:
        user = User(name=create_user.name, password_hash=create_user.password)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        # await session.refresh(user, ["tasks"])
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    return user


@user_router.patch(
    "/update", response_model=UserBaseResponse, status_code=status.HTTP_200_OK
)
async def update(
    id: int, update_user: UserUpdateRequest, session: AsyncSession = Depends(get_db)
):
    try:
        user = await session.get(User, id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id = {id} not found",
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
