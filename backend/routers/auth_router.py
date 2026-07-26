import email
import random
from signal import raise_signal
from smtplib import SMTPResponseException
import string

from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import FastMail, MessageSchema, MessageType

from dependencies import get_mail, get_session
from repository import user_repo
from repository.user_repo import EmailCodeRepository, UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import ResponseOut
from schemas.user_schema import RegisterIn, UserCreateSchema



router = APIRouter(prefix="/auth", tags="user")

@router.get("/code")
async def get_email_code(
    email: str,
    mail: FastMail = Depends(get_mail),
    session: AsyncSession = Depends(get_session)
    ):
    
    source = string.digits * 4
    code ="".join(random.sample(source, 4))
    
    msg = MessageSchema(
        subject="验证码",
        recipients=["email"],
        body="你的验证码：{code}",
        subtype=MessageType.plain
    )
    try:
        await mail.send_message(msg)
    except SMTPResponseException as e:
        if e.code == -1 and b"\x00\x00\x00" in str(e).encode():
            print("⚠️ 忽略 QQ邮箱 SMTP 关闭阶段的非标准响应（邮件已成功发送）")
            email_code_repo = EmailCodeRepository(session=session)
            await email_code_repo.create(email, code)
        else:
            raise HTTPException(status_code=500, detail="邮件发送失败")
        
        return ResponseOut()

@router.post("/register", response_model=ResponseOut)
async def register(
    data: RegisterIn,
    session: AsyncSession 
):
    user_repo = UserRepository(session=session)
    # 1.判断邮箱是否存在
    email_exist = user_repo.email_is_exist(str(data.email))
    if email_exist:
        raise HTTPException(400, detail="该邮箱已存在")
    email_code_repo = EmailCodeRepository(session=session)
    email_code_match = email_code_repo.check_email_code(str(data.email), str(data.code))
    if not email_code_match:
        raise HTTPException(400, detail="邮箱验证码错误")
    try:
        await user_repo.create(UserCreateSchema(str(data.email), str(data.password), str(data.username)))
    except Exception as e:
        raise HTTPException(500, detail=str(e))
            