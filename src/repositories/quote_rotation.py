from .base import CRUDBase
from ..models import QuoteRotation


class CRUDQuoteRotation(CRUDBase[QuoteRotation]):
    pass


rotation_repository = CRUDQuoteRotation(QuoteRotation)
