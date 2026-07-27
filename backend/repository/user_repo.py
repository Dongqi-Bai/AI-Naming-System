from datetime import datetime, timedelta

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.user import EmailCode, User
from backend.schemas.user_schema import UserCreateSchema


class EmailCodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, email: str, code: str) -> EmailCode:
        email_code = await self.session.scalar(
            select(EmailCode).where(EmailCode.email == email)
        )
        if email_code is None:
            email_code = EmailCode(email=email, code=code)
            self.session.add(email_code)
        else:
            email_code.code = code
            email_code.create_time = datetime.now()
        await self.session.commit()
        return email_code

    async def check_email_code(self, email: str, code: str) -> bool:
        stmt = select(EmailCode).where(
            EmailCode.email == email,
            EmailCode.code == code,
        )
        email_code = await self.session.scalar(stmt)
        if email_code is None:
            return False
        return datetime.now() - email_code.create_time <= timedelta(minutes=10)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        return await self.session.scalar(select(User).where(User.email == email))

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def email_is_exist(self, email: str) -> bool:
        stmt = select(exists().where(User.email == email))
        return bool(await self.session.scalar(stmt))

    async def create(self, user_schema: UserCreateSchema) -> User:
        user = User(**user_schema.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
