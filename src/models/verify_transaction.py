"""Model for verifying the status of the transaction."""

from pydantic import EmailStr
from src.models.core import CoreModel


class VerifyTransaction(CoreModel):
    """A model for verifying the transaction."""

    status: bool
    message: str
    data: dict


class SuccessfulTransaction(CoreModel):
    """A model for a successful transaction."""

    id: int
    email: EmailStr
    status: str
    reference: str
    amount: int
    paid_at: str
    created_at: str
    metadata: dict
