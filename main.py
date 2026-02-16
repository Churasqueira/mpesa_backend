from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

app = FastAPI(title="MPESA Backend")

# =====================================================
# CORS CONFIG (Resolve erro OPTIONS 405)
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, colocar domínio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# Health Check
# =====================================================
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend M-Pesa rodando!"
    }

# =====================================================
# Root
# =====================================================
@app.get("/")
def root():
    return {
        "message": "MPESA Backend ativo!"
    }

# =====================================================
# C2B Payment (Cliente paga plataforma)
# =====================================================
@app.post("/c2b-payment/")
async def c2b_payment(request: Request):
    try:
        data = await request.json()

        msisdn = data.get("msisdn")
        amount = data.get("amount")
        reference = data.get("reference")

        # Validação básica
        if not msisdn or not amount or not reference:
            return JSONResponse(
                content={
                    "error": "Campos obrigatórios: msisdn, amount, reference"
                },
                status_code=400
            )

        # Simulação de transação
        transaction_id = f"MPESA_{uuid.uuid4().hex[:8]}"
        conversation_id = f"CONV_{uuid.uuid4().hex[:8]}"

        return JSONResponse(
            content={
                "status": "SUCCESS",
                "TransactionID": transaction_id,
                "ConversationID": conversation_id,
                "ResponseCode": "INS-0",
                "ResponseDesc": "Request processed successfully"
            },
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={
                "error": str(e)
            },
            status_code=500
        )

# =====================================================
# B2C Payment (Plataforma paga cliente)
# =====================================================
@app.post("/b2c-payment/")
async def b2c_payment(request: Request):
    try:
        data = await request.json()

        msisdn = data.get("msisdn")
        amount = data.get("amount")
        reference = data.get("reference")

        if not msisdn or not amount or not reference:
            return JSONResponse(
                content={
                    "error": "Campos obrigatórios: msisdn, amount, reference"
                },
                status_code=400
            )

        transaction_id = f"MPESA_{uuid.uuid4().hex[:8]}"
        conversation_id = f"CONV_{uuid.uuid4().hex[:8]}"

        return JSONResponse(
            content={
                "status": "SUCCESS",
                "TransactionID": transaction_id,
                "ConversationID": conversation_id,
                "ResponseCode": "INS-0",
                "ResponseDesc": "Payout processed successfully"
            },
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={
                "error": str(e)
            },
            status_code=500
        )

# =====================================================
# Transaction Status (Simulado)
# =====================================================
@app.get("/transaction-status/{reference}/")
def transaction_status(reference: str):
    return {
        "reference": reference,
        "status": "SUCCESS",
        "TransactionID": f"MPESA_{reference}",
        "amount": 50,
        "msisdn": "258843330333"
    }
