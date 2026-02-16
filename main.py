from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import requests

app = FastAPI(title="MPESA Backend")

# =========================
# Health Check
# =========================
@app.get("/health")
def health_check():
    return {"status": "ok"}

# =========================
# Página raiz
# =========================
@app.get("/")
def root():
    return {"message": "MPESA Backend ativo!"}

# =========================
# Rota de pagamento C2B
# =========================
@app.post("/c2b-payment/")
async def c2b_payment(request: Request):
    """
    Recebe pagamentos C2B do Mpesa.
    Substitua esta função com sua lógica real de processamento.
    """
    try:
        data = await request.json()
        print("Pagamento recebido:", data)

        # =========================
        # Exemplo: enviar dados para API Mpesa (preencher detalhes reais)
        # =========================
        mpesa_api_url = os.getenv("MPESA_API_URL", "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate")
        mpesa_token = os.getenv("MPESA_API_TOKEN", "SEU_TOKEN_AQUI")

        headers = {
            "Authorization": f"Bearer {mpesa_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "ShortCode": data.get("ShortCode", "600000"),
            "CommandID": data.get("CommandID", "CustomerPayBillOnline"),
            "Amount": data.get("Amount", 1),
            "Msisdn": data.get("Msisdn", "254700000000"),
            "BillRefNumber": data.get("BillRefNumber", "Teste001")
        }

        # Envia requisição para Mpesa (descomente quando estiver pronto)
        # response = requests.post(mpesa_api_url, json=payload, headers=headers)
        # return JSONResponse(content={"status": "success", "mpesa_response": response.json()})

        # Por enquanto, apenas retorna o payload recebido
        return JSONResponse(content={"status": "success", "data": payload})

    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=400)
