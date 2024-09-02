from .base import CRUDBase
from ..models import Chug


class CRUDChug(CRUDBase[Chug]):
    pass

chug_repository = CRUDChug(Chug)
