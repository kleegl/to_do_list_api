from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


@as_declarative()
class Base:
    pass


engine = create_async_engine(
    "postgresql+asyncpg://root:root@localhost/to_do_list",
    echo=True,
)


SessionLocal = sessionmaker(
    engine, class_=AsyncSession, autoflush=False, autocommit=False
)


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            session.close()
