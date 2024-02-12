from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
import app.models as models
import app.oath2 as oath2
from app.models import *
from app.schemas import *
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils import *
from app.oath2 import *

router = APIRouter( prefix = "/vote", tags = ['Vote'])

@router.post('/', status_code= status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user : int = Depends(oath2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {vote.post_id} does not exist')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
    models.Vote.user_id == current_user.id) # this line checks if this user already liked that specific post before

    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail =  f'{current_user.id} has already voted on post {vote.post_id}')
        
        new_vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return{"successfully added vote"}   
        
    else:
         if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =  f'{current_user.id}  has voted on post {vote.post_id}')
         
         vote_query.delete(synchronize_session = False)
         db.commit()

         return{"successfully removed vote"}
