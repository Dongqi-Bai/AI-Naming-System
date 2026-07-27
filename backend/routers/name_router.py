from fastapi import APIRouter, Depends

from backend.core.agent import generate_names
from backend.dependencies import get_current_user
from backend.models.user import User
from backend.schemas.name import NameIn, NameOut


router = APIRouter(prefix="/name", tags=["AI 起名"])


@router.post("", response_model=NameOut)
async def take_name(
    name_info: NameIn,
    _: User = Depends(get_current_user),
):
    result = await generate_names(name_info)
    return NameOut(names=result.names)
