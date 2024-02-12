from typing import List
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import app.models as models
import app.oath2 as oath2
from app.models import *
from app.schemas import *
from app.utils import *
from app.database import get_db
from sqlalchemy.orm import Session 
from app.oath2 import *


router = APIRouter( tags = ['login'])

@router.post('/login', response_model= Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):

    #oauth2 return 2 fields as 'username' and 'password'

    # first, we find the account from the email given
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # if email is not in database, return invalid credentials
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 'Invalid credentials')
    
    # if email is correct but the hashed version of the password given does not match the one in the database
    # return invalid credentials

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 'Invalid credentials')
    
    #if all is correct, create and return token

    access_token = oath2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token,"token_type" : "bearer"}

