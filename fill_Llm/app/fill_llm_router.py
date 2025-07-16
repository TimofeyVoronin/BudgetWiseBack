from fastapi import APIRouter
from app.auto_fill_llm import AutoFillLLM
from app.input_Protect.validation_input import ReqProductsLLM



productsLLM = APIRouter(prefix = "/api/autofill_llm",tags=["Send this into a AutoFillLLM"])
autoFillLLM = AutoFillLLM()

'''

autoFillLLM.tokenVerification(token=ReqProductsLLM.userToken,userId=ReqProductsLLM.userID) - 
Раскомменти для того чтобы была проверка токена

'''



#Router
@productsLLM.post("/setCategory")
def sendToChequeInfo(reqProductsLLM: ReqProductsLLM):
    #autoFillLLM.tokenVerification(token=ReqProductsLLM.userToken,userId=ReqProductsLLM.userID)
    categories = autoFillLLM.getCategory(reqProductsLLM)
    return categories


@productsLLM.post("/setProductsTypes")
def sendToChequeInfo(reqProductsLLM: ReqProductsLLM):
    #autoFillLLM.tokenVerification(token=ReqProductsLLM.userToken,userId=ReqProductsLLM.userID)
    productType = autoFillLLM.getProductType(reqProductsLLM)
    return productType



