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
def setCategory(reqProductsLLM: ReqProductsLLM):
    #autoFillLLM.tokenVerification(token=reqProductsLLM.userToken,userId=reqProductsLLM.userID)
    categories = autoFillLLM.getCategory(reqProductsLLM,transactionID=reqProductsLLM.transactionID)
    requests.post(url=f"http://django:8000/api/transactions/{reqProductsLLM.transactionID}/set-category/", data = categories)#send category transaction to the db
    return "Send successfull"

@productsLLM.post("/setProductsTypes")
def setProductsTypes(reqProductsLLM: ReqProductsLLM):
    #autoFillLLM.tokenVerification(token=ReqProductsLLM.userToken,userId=ReqProductsLLM.userID)
    positionsCategory = autoFillLLM.getPrositionCategory(reqProductsLLM)
    requests.post(url=f"http://django:8000/api/transactions/{reqProductsLLM.transactionID}/positions/bulk-set-category/", data=positionsCategory)#send category products to the db
    return "Send successfull"



