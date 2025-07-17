from fastapi import APIRouter
from app.auto_fill_llm import AutoFillLLM
from app.input_Protect.validation_input import ReqProductsLLM
import requests



productsLLM = APIRouter(prefix = "/api/autofill_llm",tags=["Send this into a AutoFillLLM"])
autoFillLLM = AutoFillLLM()

'''

autoFillLLM.tokenVerification(token=ReqProductsLLM.userToken,userId=ReqProductsLLM.userID) - 
Раскомменти для того чтобы была проверка токена

'''



#Router
@productsLLM.post("/setCategory")
def sendToChequeInfo(reqProductsLLM: ReqProductsLLM):
    #autoFillLLM.tokenVerification(token=reqProductsLLM.userToken,userId=reqProductsLLM.userID)
    categories = autoFillLLM.getCategory(reqProductsLLM,transactionID=reqProductsLLM.transactionID)
    request.post(url=)


@productsLLM.post("/setProductsTypes")
def sendToChequeInfo(reqProductsLLM: ReqProductsLLM):
    #autoFillLLM.tokenVerification(token=ReqProductsLLM.userToken,userId=ReqProductsLLM.userID)
    productType = autoFillLLM.getProductType(reqProductsLLM,transactionID=reqProductsLLM.transactionID)
    return productType



