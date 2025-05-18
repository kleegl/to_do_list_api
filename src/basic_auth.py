from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
import bcrypt


from core import get_db
from models import User
from response import UserBaseResponse

bcrypt.__about__ = bcrypt
basic_security = HTTPBasic()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def verify_credentials(
    credentials: HTTPBasicCredentials = Depends(basic_security),
    session: AsyncSession = Depends(get_db),
):
    stmt = select(User).where(User.name == credentials.username)
    user = (await session.execute(stmt)).scalar_one_or_none()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return UserBaseResponse(id=user.id, name=user.name)
