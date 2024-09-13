from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/v1")


class Version(BaseModel):
    version: str = Field("1.0")


@router.get("/")
async def version() -> Version:
    return {"version": "1.0"}
