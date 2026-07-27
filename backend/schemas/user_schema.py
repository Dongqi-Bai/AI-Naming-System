from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class RegisterIn(BaseModel):
    email: EmailStr
    username: Annotated[str, Field(min_length=2, max_length=20, description="用户名")]
    password: Annotated[str, Field(min_length=6, max_length=64, description="密码")]
    confirm_password: Annotated[
        str,
        Field(min_length=6, max_length=64, description="确认密码"),
    ]
    code: Annotated[str, Field(pattern=r"^\d{4}$", description="邮箱验证码")]

    @model_validator(mode="after")
    def password_is_match(self) -> "RegisterIn":
        if self.password != self.confirm_password:
            raise ValueError("两次输入的密码不一致")
        return self


class UserCreateSchema(BaseModel):
    email: EmailStr
    username: Annotated[str, Field(min_length=2, max_length=20)]
    password: Annotated[str, Field(min_length=6, max_length=64)]


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str


class LoginIn(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=6, max_length=64)]


class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserSchema
