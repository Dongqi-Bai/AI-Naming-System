import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_mail import FastMail
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.auth import decode_access_token
from backend.core.mail import create_mail_instance
from backend.models import AsyncSessionFactory
from backend.models.user import User
from backend.repository.user_repo import UserRepository


bearer_scheme = HTTPBearer(auto_error=False)


async def get_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session


async def get_mail() -> FastMail:
    return create_mail_instance()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="登录状态已失效，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, TypeError, ValueError):
        raise unauthorized

    user = await UserRepository(session).get_by_id(user_id)
    if user is None:
        raise unauthorized
    return user
