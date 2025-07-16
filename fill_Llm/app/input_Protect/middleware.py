import os
from jose import jwt
from fastapi import HTTPException

class MiddleWare:
    __secretKey = os.getenv("SECRET_KEY")
    def tokenVerification(self,token,userId):
        try:
            deCode = jwt.decode(token=token, key=self.__secretKey, algorithms="HS256")
            if(deCode!=userId["user"]):#?
                raise HTTPException(status_code=401, detail="Invalid token") 
            return True
        except Exception:
            raise HTTPException(status_code=401, detail="Expired token")