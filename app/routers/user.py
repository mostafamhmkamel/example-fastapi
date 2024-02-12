from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
import app.models as models
from app.models import *
from app.schemas import *
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils import *


router = APIRouter( prefix = "/users",tags = ['Users'])


#get all users



#get specific user

@router.get('/{id}', response_model= UserResponse)
def get_user(id: int,  db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail = f'user with id: {id} was not found')
    return user
    
#create user

@router.post('/', status_code= status.HTTP_201_CREATED, response_model= UserResponse) #the below format is important to avoid SQL injection
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    #hashing password

    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = models.User(email= user.email, password = user.password) # **post.dict() to get everything
    db.add(new_user) #adding the newly created post into the database
    db.commit() #committing change into the database
    db.refresh(new_user) #retrieves new post


    return new_user



