from pydantic import BaseModel, Field

#Thing which uses to send info in auto_fill_LLM, especially items from cheque
class ReqProductsLLM(BaseModel):
    userToken: str = Field(default=...,description="Access token")
    userID: int = Field(default=...)
    transactionID: int
    items: list = [
        {"name": str,  
        "productType": str,
        "quantity": int,
        "price": float,
        "sum": float}
        ]