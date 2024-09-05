from .base import CRUDBase
from ..models import Card


class CRUDCard(CRUDBase[Card]):
    pass

card_repository = CRUDCard(Card)
