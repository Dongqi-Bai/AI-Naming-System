from datetime import datetime, timedelta

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.user import EmailCode, User
from schemas.user_schema import UserCreateSchema


class EmailCodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create(self, email: str, code: str) -> EmailCode:
        async with self.session.begin():
            email_code = EmailCode(email=email, code=code)
            self.session.add(email_code)
            return email_code
        
    async def check_email_code(self, email: str, code: str) -> bool:
        async with self.session.begin():
            stmt = select(EmailCode).where(EmailCode.email == email,
            EmailCode.code == code)
            email_code: EmailCode | None = await self.session.scalar(stmt)
            if email_code is None:
                return False
            if (datetime.now() - email_code.created_time) > timedelta(minutes=10):
                return False
            return True    
               
               
class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_email(self, email: str) -> User:
        async with self.session.begin():
            return await self.session.scalar(select(User).filter(User.email==email))
        
    async def email_is_exist(self, email: str) -> bool:
        async with self.session.begin():
            stmt = select(exists().where(User.email==email))
            return await self.session.scalar(stmt)
    
    async def create(self, user_schema: UserCreateSchema) -> User:
        async with self.session.begin():
            user = User(**user_schema.model_dump())
            self.session.add(user)
            return user