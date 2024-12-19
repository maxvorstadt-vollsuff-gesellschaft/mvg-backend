from pydantic import BaseModel


class MemberBase(BaseModel):
    name: str


class MemberCreate(MemberBase):
    pass


class Member(MemberCreate):
    id: int
    user_sub: str
    tkt_elo_rating: float
    
    class Config:
        from_attributes = True
