

from fastapi import APIRouter

from core.agent import generate_names
from schemas.name import NameIn, NameOut


router = APIRouter(prefix="/name", tags=["name"])

@router.post("/name", response_model=NameOut)
async def take_name(name_info: NameIn):
    result = await generate_names(name_info)
    return NameOut(names=result.names)