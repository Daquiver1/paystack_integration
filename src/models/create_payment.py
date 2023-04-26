"""Model for creating a payment."""
from src.models.core import CoreModel


class CreatePayment(CoreModel):
    """A model for creating payment."""

    authorization_url: str
    access_code: str
    reference: str
