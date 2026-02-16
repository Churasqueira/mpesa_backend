from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import base64

app = FastAPI(title="MPESA Vodacom Mozambique Backend")

# ===============================
# CORS
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste se precisar restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# ENV Variables
# ===============================
API_KEY = os.getenv("MPESA_API_KEY")  # ex: 4lenul0e961hp38j32xqey1vwjnvxznt
PUBLIC_KEY = os.getenv("MPESA_PUBLIC_KEY")  # sua public key RSA
SERVICE_PROVIDER_CODE = os.getenv("MPESA_SERVICE_PROVIDER_CODE", "171717")
BASE_URL = os.getenv("MPESA_BASE_URL", "https://sandbox.vm.co.mz")  # sandbox ou produção

# ===============================
# Health Check
# ===============================
@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend M-Pesa Vodacom rodando!"}

# ===============================
# Gerar token Bearer
# ===============================
def generate_token():
    url = f"{BASE_URL}/ipg/v1x/oauth2/generate?grant_type=client_credentials"
    encoded = base64.b64encode(f"{API_KEY}:".encode()).decode()
    headers = {"Authorization": f"Basic {encoded}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json().get("access_token")
    raise Exception(f"Erro ao gerar token: {resp.text}")

# ===============================
# Pagamento C2B (Cliente paga Plataforma)
# ===============================
@app.post("/c2b-payment/")
async def c2b_payment(request: Request):
    try:
        data = await request.json()
        msisdn = data.get("msisdn")
        amount = str(data.get("amount"))
        reference = data.get("reference")
        if not msisdn or not amount or not reference:
            return JSONResponse({"error": "Campos obrigatórios ausentes"}, status_code=400)

        token = generate_token()
        url = f"{BASE_URL}/ipg/v1x/c2bPayment/singleStage/"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {
            "input_TransactionReference": reference,
            "input_CustomerMSISDN": msisdn,
            "input_Amount": amount,
            "input_ThirdPartyReference": reference,
            "input_ServiceProviderCode": SERVICE_PROVIDER_CODE
        }
        resp = requests.post(url, json=payload, headers=headers)
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ===============================
# Pagamento B2C (Plataforma paga Cliente)
# ===============================
@app.post("/b2c-payment/")
async def b2c_payment(request: Request):
    try:
        data = await request.json()
        msisdn = data.get("msisdn")
        amount = str(data.get("amount"))
        reference = data.get("reference")
        if not msisdn or not amount or not reference:
            return JSONResponse({"error": "Campos obrigatórios ausentes"}, status_code=400)

        token = generate_token()
        url = f"{BASE_URL}/ipg/v1x/b2cPayment/"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {
            "input_TransactionReference": reference,
            "input_CustomerMSISDN": msisdn,
            "input_Amount": amount,
            "input_ThirdPartyReference": reference,
            "input_ServiceProviderCode": SERVICE_PROVIDER_CODE
        }
        resp = requests.post(url, json=payload, headers=headers)
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
