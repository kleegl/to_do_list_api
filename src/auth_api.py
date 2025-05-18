from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from basic_auth import get_password_hash
from core import get_db
from models import User
from request import UserCreateRequest


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
async def register(
    create_user: UserCreateRequest, session: AsyncSession = Depends(get_db)
):
    try:
        existing_user = await session.execute(
            select(User).where(User.name == create_user.name)
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail=f"User with name {create_user.name} already existed!",
            )

        hashed_pwd = await get_password_hash(create_user.password)

        user = User(name=create_user.name, password_hash=hashed_pwd)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    return user
