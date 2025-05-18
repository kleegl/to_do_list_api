from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from basic_auth import get_password_hash
from models import User


async def create_admin(session: AsyncSession):
    admin_name = "admin"
    admin_pwd = "admin"

    existing_admin = await session.execute(select(User).where(User.name == admin_name))

    if not existing_admin.scalar_one_or_none():
        admin = User(
            name=admin_name, password_hash=get_password_hash(admin_pwd), is_admin=True
        )
        session.add(admin)
        await session.commit()
