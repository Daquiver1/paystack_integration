"""Route to accept user payments."""

import hashlib
import hmac
import json

import requests
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from src.core.config import PAYSTACK_SECRET_KEY_DEV, PAYSTACK_SECRET_KEY_PROD
from src.models.create_payment import CreatePayment
from src.models.verify_transaction import VerifyTransaction

router = APIRouter()


@router.post(
    "/create-payment",
    response_model=CreatePayment,
)
async def create_payment(email: str, amount: float):
    """Create payment."""
    try:
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY_DEV}",
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning": "true",
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
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid error")


def callback_function(response):
    print("Response has been triggered. ")
    print(response)
    return response


@router.get(
    "/verify_transaction",
    # skip_browser_warning_header=Depends(skip_browser_warning_header),
    response_model=VerifyTransaction,
)
async def verify_transaction(reference: str):
    """Verify transaction."""
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY_DEV}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response


@router.post("/paystack/webhook")
async def paystack_webhook(request: Request, response: Response) -> JSONResponse:
    """Paystack webhook url."""
    event = json.loads(await request.body())
    event_type = event["event"]

    print("Webhook was triggered. ")
    # Retrieve the request's body
    body = await request.body()
    payload = body.decode()

    # Retrieve the value of the x-paystack-signature header
    signature = request.headers.get("x-paystack-signature")

    # Validate the signature
    computed_signature = hmac.new(
        PAYSTACK_SECRET_KEY_DEV.encode(), msg=payload.encode(), digestmod=hashlib.sha512
    ).hexdigest()

    if signature == computed_signature:
        # Signature is valid, process the event
        event = await request.json()
        # Do something with event

        if event_type == "charge.success":
            # handle the completed transaction here
            print("It was successful.")
            transaction_id = event["data"]["id"]
            amount = event["data"]["amount"]
            email = event["data"]["customer"]["email"]
            print(transaction_id, amount, email)
            # you can perform additional actions here, such as updating your
            #  database or sending an email notification

        return JSONResponse(
            content={"message": "Webhook received successfully"}, status_code=200
        )

    return JSONResponse(content={"message": "Invalid signature"}, status_code=404)


@router.post("/create_plan")
async def create_plan(name: str, amount: float):
    """Creating a plan"""
    url = "https://api.paystack.co/plan"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY_DEV}",
        "Content-Type": "application/json",
    }
    data = {
        "amount": amount * 100,
        "interval": "monthly",
        "name": name,
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    print(response)
    if response.status_code == 201:
        return response.json()["data"]
    else:
        return response.json()["message"]


@router.post("/subscribe_plan")
async def subscribe_plan(email: str, amount: float):
    """Subscribe to plan."""
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY_DEV}",
        "Content-Type": "application/json",
    }
    data = {
        "amount": amount * 100,
        "email": email,
        "channels": ["mobile_money"],
        "plan": "PLN_467xrctrfv79mu3",
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    print(response)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return response.json()["message"]


# @router.post("/paystack/webhook")
# async def paystack_webhook(request: Request, response: Response):
#     event = json.loads(await request.body())
#     event_type = event["event"]

#     if event_type == "charge.success":
#         # handle the completed transaction here
#         transaction_id = event["data"]["id"]
#         amount = event["data"]["amount"]
#         email = event["data"]["customer"]["email"]
#         # you can perform additional actions here, such as updating your database or sending an email notification

#     return JSONResponse(
#         content={"message": "Webhook received successfully"}, status_code=200
#     )
