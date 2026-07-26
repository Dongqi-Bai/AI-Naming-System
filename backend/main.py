from fastapi import Depends, FastAPI
from fastapi_mail import FastMail, MessageSchema, MessageType
from backend.dependencies import get_mail
from backend.routers.auth_router import router as auth_router
from backend.routers.name_router import router as name_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(name_router)


# @app.get("mail/test")
# async def mail_test(
#     email: str,
#     mail: FastMail = Depends(get_mail)
# ):
#     msg = MessageSchema(
#         subject="验证码",
#         recipients=["email"],
#         body="你的验证码：123456",
#         subtype=MessageType.plain
#     )
#     await mail.send_message(msg)
#     return {"message":"邮件发送成功"}