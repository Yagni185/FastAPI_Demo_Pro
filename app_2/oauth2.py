from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import models, schemas
from sqlalchemy.orm import Session
from app_2.database import get_db
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import setting
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'auth1')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'authuser5')

#SECRET_KEY
#Alogorithm
#Expriation time

SECRET_KEY = setting.secret_key
ALOGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALOGORITHM)
    
    return encoded_jwt

def verify_access_token(token : str, credentials_exception):
    try:
        # print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALOGORITHM])
        id : str = payload.get("user_id")
        if id is None:
            raise credentials_exception 
        token_data = schemas.TokenData(id = id)  
    except JWTError:
        # print(e)
        raise credentials_exception
    # except AssertionError as e:
    #     print(e)
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers= {"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    a = db.query(models.Login).filter(models.Login.id == token.id).first()
    return a
    # return verify_access_token(token, credentials_exception)

def get_current_user1(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f"Could not validate credentials", headers= {"WWW-Authenticate" : "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    a = db.query(models.User1).filter(models.User1.id == token.id).first()
    return a