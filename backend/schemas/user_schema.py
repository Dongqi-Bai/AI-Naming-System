from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, model_validator


class RegisterIn(BaseModel):
    email: EmailStr
    username: Annotated[str, Field(..., min_length=4, max_length=20, description="用户名")]
    password: Annotated[str, Field(..., min_length=6, max_length=20, description="密码")]
    confirm_password: Annotated[str, Field(..., min_length=6, max_length=20, description="密码")]
    code: Annotated[str, Field(..., min_length=4, max_length=4, description="验证码")]
    
    @model_validator(mode="after")
    def password_is_match(self) -> "RegisterIn":
        password = self.password
        confirm_password = self.confirm_password
        if password != confirm_password:
            raise ValueError("密码不一致")
        return self
    
class UserCreateSchema(BaseModel):
    email: EmailStr
    username: Annotated[str, Field(..., min_length=4, max_length=20, description="用户名")]
    password: Annotated[str, Field(..., min_length=6, max_length=20, description="密码")]    
    
    
class UserSchema(BaseModel):
    username: Annotated[str, Field(..., min_length=4, max_length=20, description="用户名")]
    password: Annotated[str, Field(..., min_length=6, max_length=20, description="密码")] 