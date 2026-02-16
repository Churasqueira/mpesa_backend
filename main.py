import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="M-Pesa Backend")

API_KEY = os.getenv("MPESA_API_KEY")
PUBLIC_KEY = os.getenv("MPESA_PUBLIC_KEY")
SERVICE_PROVIDER_CODE = os.getenv("MPESA_SERVICE_PROVIDER_CODE", "171717")

class PaymentRequest(BaseModel):
    msisdn: str
    amount: float
    reference: str

@app.post("/c2b-payment/")
def c2b_payment(request: PaymentRequest):
    url = "https://api.sandbox.vm.co.mz/ipg/v1x/c2bPayment/singleStage/"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Origin": "*"
    }
    payload = {
        "input_TransactionReference": request.reference,
        "input_CustomerMSISDN": request.msisdn,
        "input_Amount": str(request.amount),
        "input_ThirdPartyReference": request.reference,
        "input_ServiceProviderCode": SERVICE_PROVIDER_CODE
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()
