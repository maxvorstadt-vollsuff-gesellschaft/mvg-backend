from .member import Member
from pydantic import BaseModel


class BaseChug(BaseModel):
    member: Member
    time: int

    class Config:
        from_attributes = True


class UploadChug(BaseModel):
    id: list[str]
    time: list[int]
