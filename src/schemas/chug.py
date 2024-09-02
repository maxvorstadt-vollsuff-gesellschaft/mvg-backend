from .member import Member
from pydantic import BaseModel


class BaseChug(BaseModel):
    member: Member
    time: int


class UploadChug(BaseModel):
    id: list[int]
    time: list[int]
