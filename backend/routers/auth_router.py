import random
import string

from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.auth import create_access_token
from backend.dependencies import get_current_user, get_mail, get_session
from backend.models.user import User
from backend.repository.user_repo import EmailCodeRepository, UserRepository
from backend.schemas import ResponseOut
from backend.schemas.user_schema import (
    LoginIn,
    LoginOut,
    RegisterIn,
    UserCreateSchema,
    UserSchema,
)


router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/code", response_model=ResponseOut)
async def get_email_code(
    email: EmailStr,
    mail: FastMail = Depends(get_mail),
    session: AsyncSession = Depends(get_session),
):
    email_text = str(email)
    if await UserRepository(session).email_is_exist(email_text):
        raise HTTPException(status_code=400, detail="该邮箱已注册")

    code = "".join(random.choices(string.digits, k=4))
    message = MessageSchema(
        subject="AI 起名注册验证码",
        recipients=[email_text],
        body=f"你的验证码是：{code}。验证码 10 分钟内有效。",
        subtype=MessageType.plain,
    )
    try:
        await mail.send_message(message)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="验证码发送失败，请检查邮箱配置",
        ) from exc

    await EmailCodeRepository(session).create(email_text, code)
    return ResponseOut(message="验证码已发送")


@router.post("/register", response_model=ResponseOut)
async def register(
    data: RegisterIn,
    session: AsyncSession = Depends(get_session),
):
    user_repo = UserRepository(session)
    email = str(data.email)
    if await user_repo.email_is_exist(email):
        raise HTTPException(status_code=400, detail="该邮箱已注册")
    if not await EmailCodeRepository(session).check_email_code(email, data.code):
        raise HTTPException(status_code=400, detail="邮箱验证码错误或已过期")

    try:
        await user_repo.create(
            UserCreateSchema(
                email=email,
                password=data.password,
                username=data.username,
            )
        )
    except Exception as exc:
        await session.rollback()
        raise HTTPException(status_code=500, detail="注册失败，请稍后重试") from exc
    return ResponseOut(message="注册成功")


@router.post("/login", response_model=LoginOut)
async def login(
    data: LoginIn,
    session: AsyncSession = Depends(get_session),
):
    user = await UserRepository(session).get_by_email(str(data.email))
    if user is None or not user.verify_password(data.password):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    return LoginOut(
        access_token=create_access_token(user.id, user.email),
        user=UserSchema.model_validate(user),
    )


@router.get("/me", response_model=UserSchema)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserSchema.model_validate(current_user)
