from .base import CRUDBase
from ..models import Member


class CRUDMember(CRUDBase[Member]):
    pass


member_repository = CRUDMember(Member)
