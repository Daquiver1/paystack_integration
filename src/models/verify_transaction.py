"""Model for verifying the status of the transaction."""

from src.models.core import CoreModel


class VerifyTransaction(CoreModel):
    """A model for verifying the transaction."""

    status: bool
    message: str
    data: dict
