from pydantic import BaseModel


class MemberBase(BaseModel):
    name: str


class MemberCreate(MemberBase):
    pass


class Member(MemberCreate):
    id: int

    class Config:
        from_attributes = True
