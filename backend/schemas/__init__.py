from typing import Annotated, Literal

from pydantic import BaseModel, Field


class ResponseOut(BaseModel):
    result: Annotated[
        Literal["success", "failure"],
        Field(default="success", description="操作结果"),
    ]
    message: str = "操作成功"
