"""Route to accept user payments."""

import hashlib
import hmac
import json

import requests
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from src.core.config import BASE_URL, PAYSTACK_SECRET_KEY
from src.models.create_payment import CreatePayment
from src.models.verify_transaction import SuccessfulTransaction, VerifyTransaction

router = APIRouter()


@router.post(
    "/create-payment",
    response_model=CreatePayment,
)
async def create_payment(email: str, amount: float) -> CreatePayment:
    """
    This function creates a mobile money payment transaction using the Paystack API with the specified email and
    amount.
    """
    try:
        url = f"{BASE_URL}transaction/initialize"
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
            return response.json()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid error")


@router.get(
    "/verify_transaction",
    response_model=VerifyTransaction,
)
async def verify_transaction(reference: str) -> VerifyTransaction:
    """This function verifies a paystack transaction. It returns the status of the transaction."""
    try:
        url = f"{BASE_URL}transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid error")


@router.post("/paystack/webhook")
async def paystack_webhook(request: Request, response: Response) -> JSONResponse:
    """This function creates a webhook, that'll receive a response from Paystack."""
    payload = await request.body()
    signature = request.headers.get("x-paystack-signature")

    computed_signature = hmac.new(
        PAYSTACK_SECRET_KEY.encode(), msg=payload, digestmod=hashlib.sha512
    ).hexdigest()

    if signature != computed_signature:
        return JSONResponse(content={"message": "Invalid signature"}, status_code=404)

    event = await request.json()

    transaction_id = event["data"]["id"]
    amount = event["data"]["amount"]
    email = event["data"]["customer"]["email"]
    print(event["data"])
    print(SuccessfulTransaction(**event["data"]))
    print(transaction_id, amount, email)

    return JSONResponse(
        content={"message": "Transaction was successful."}, status_code=200
    )


@router.post("/create_plan")
async def create_plan(name: str, amount: float):
    """This function creates a monthly paystack subscription plan."""
    try:
        url = f"{BASE_URL}plan"
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "amount": amount * 100,
            "interval": "monthly",
            "name": name,
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()["data"]
        else:
            return response.json()["message"]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid error")


@router.post("/subscribe_plan")
async def subscribe_plan(email: str, subscription_plan: str, amount: float):
    """This functions subscribes to a paystack plan."""
    try:
        url = f"{BASE_URL}transaction/initialize"
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "amount": amount * 100,
            "email": email,
            "channels": ["card"],
            "plan": subscription_plan,
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return response.json()["message"]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid error")
