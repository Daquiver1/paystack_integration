"""Route to accept user payments."""

import json

import requests
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from src.core.config import PAYSTACK_SECRET_KEY
from src.models.create_payment import CreatePayment
from src.models.verify_transaction import VerifyTransaction

router = APIRouter()


@router.post("/create-payment", response_model=CreatePayment)
async def create_payment(email: str, amount: float):
    """Create payment."""
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "amount": amount * 100,
        "email": email,
        "currency": "GHS",
        "channels": ["mobile_money"],
        "metadata": {
            "custom_fields": [
                {
                    "display_name": "Telegram Username",
                    "variable_name": "Telegram Username",
                    "value": "Daquiver",
                },
                {
                    "display_name": "Telegram ID",
                    "variable_name": "10829272",
                    "value": "10829272",
                },
            ]
        },
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200 and response.json()["status"] is True:
        print(response.json())
        return response.json()["data"]
    else:
        return response


@router.get("/verify_transaction", response_model=VerifyTransaction)
async def verify_transaction(reference: str):
    """Verify transaction."""
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response


@router.post("/paystack/webhook")
async def paystack_webhook(request: Request, response: Response):
    event = json.loads(await request.body())
    event_type = event["event"]

    if event_type == "charge.success":
        # handle the completed transaction here
        transaction_id = event["data"]["id"]
        amount = event["data"]["amount"]
        email = event["data"]["customer"]["email"]
        # you can perform additional actions here, such as updating your database or sending an email notification

    return JSONResponse(
        content={"message": "Webhook received successfully"}, status_code=200
    )
