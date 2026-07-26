from fastapi_mail import FastMail
from backend.core.mail import create_mail_instance
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models import AsyncSessionFactory

async def get_session() -> AsyncSession:
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()

async def get_mail() -> FastMail:
    return create_mail_instance()