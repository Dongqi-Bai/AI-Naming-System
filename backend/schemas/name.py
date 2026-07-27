from typing import Annotated, Literal

from pydantic import BaseModel, Field

from backend.schemas.agent import NameSchema


class NameIn(BaseModel):
    surname: Annotated[str, Field(min_length=1, max_length=4, description="姓氏")]
    gender: Annotated[Literal["不限", "男", "女"], Field(description="性别")]
    length: Annotated[
        Literal["不限", "单字", "双字"],
        Field(description="名字字数"),
    ]
    other: Annotated[
        str | None,
        Field(default="", max_length=200, description="其他要求"),
    ]
    exclude: Annotated[
        list[str],
        Field(default_factory=list, description="排除的名字或用字"),
    ]


class NameOut(BaseModel):
    names: list[NameSchema]
