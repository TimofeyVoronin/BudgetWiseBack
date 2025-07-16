from fastapi import FastAPI

from app.fill_llm_router import productsLLM

llm = FastAPI()
llm.include_router(productsLLM)



@llm.get("/")
def root():
    return {"Main page"}
    

