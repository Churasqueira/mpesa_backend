from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from portalsdk import APIContext, APIMethodType, APIRequest

# Inicializa FastAPI
app = FastAPI(title="M-Pesa Backend")

# Dados do M-Pesa do .env
API_KEY = os.getenv("MPESA_API_KEY")
PUBLIC_KEY = os.getenv("MPESA_PUBLIC_KEY")
SERVICE_PROVIDER_CODE = os.getenv("MPESA_SERVICE_PROVIDER_CODE", "171717")  # exemplo

# Modelo para requisição de pagamento
class PaymentRequest(BaseModel):
    msisdn: str
    amount: float
    reference: str

@app.post("/c2b-payment/")
def c2b_payment(request: PaymentRequest):
    try:
        context = APIContext()
        context.api_key = API_KEY
        context.public_key = PUBLIC_KEY
        context.ssl = True
        context.method_type = APIMethodType.POST
        context.address = "api.sandbox.vm.co.mz"
        context.port = 18352
        context.path = "/ipg/v1x/c2bPayment/singleStage/"
        context.add_header("Origin", "*")
        
        context.add_parameter("input_TransactionReference", request.reference)
        context.add_parameter("input_CustomerMSISDN", request.msisdn)
        context.add_parameter("input_Amount", str(request.amount))
        context.add_parameter("input_ThirdPartyReference", request.reference)
        context.add_parameter("input_ServiceProviderCode", SERVICE_PROVIDER_CODE)
        
        api_request = APIRequest(context)
        response = api_request.execute()

        return {
            "status_code": response.status_code,
            "result": response.result,
            "parameters": response.parameters
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
