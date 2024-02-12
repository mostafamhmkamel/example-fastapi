from typing import List, Optional
from sqlalchemy import func
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
import app.models as models
import app.oath2 as oath2
from app.models import *
from app.schemas import *
from app.utils import *
from app.database import get_db
from sqlalchemy.orm import Session 
from app.oath2 import *




router = APIRouter(prefix = "/posts", tags = ['Posts'])

#below request should get all posts
#except when user applies the different query parameters (e.g. limits, etc..)

@router.get("/", response_model= List[PostOut]) #code below uses the session connection to apply query on database and return it's data
def get_posts(db: Session = Depends(get_db), user_id : int = Depends(oath2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str] = '' ): 

    #limit: limits returned posts, while offset skips the number of posts you give it
    #contains: filters posts with strings that you input
    # example url of search function by user: /posts?limit=1&search=hotmail
    # %20 is equivalen to a space in a url


    #outer join which returns posts with number of likes (using group by and count in query)

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
        isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

#create post
# notice the dependency at the end, it will call that function to find out if user has valid token and what his id is

@router.post('/', status_code= status.HTTP_201_CREATED, response_model= PostResponse) #the below format is important to avoid SQL injection
def create_post(post: PostBase, db: Session = Depends(get_db), current_user : int = Depends(oath2.get_current_user)):


    new_post = models.Post(owner_id = current_user.id, title= post.title, content = post.content, published = post.published) # **post.dict() to get everything
    db.add(new_post) #adding the newly created post into the database
    db.commit() #committing change into the database
    db.refresh(new_post) #retrieves new post

    return new_post

#get specific post

@router.get('/{id}', response_model= PostOut)
def get_post(id: int, db: Session = Depends(get_db), user_id : int = Depends(oath2.get_current_user) ):

    post = posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
        isouter = True).group_by(models.Post.id).first() #returns first row where statement is true

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail = f'post with id: {id} was not found')
    return post

#delete post
#notice that current_user takes type int, this doesn't actually matter. it's filler

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    #checks if post exists

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail = f'post with id: {id} was not found')
    
    #check if the post belongs to the person who wants to delete

    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f'not authorize to perform action')
    
    post_query.delete(synchronize_session = False)
    db.commit()

    return {Response(status_code=status.HTTP_204_NO_CONTENT)}

#update post

@router.put('/{id}', response_model= PostResponse)
def update_post(id: int, updated_post: PostCreate,  db: Session = Depends(get_db), current_user : int = Depends(oath2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first() 

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail = f'post with id: {id} was not found')
    
    #check if the post belongs to the person who wants to update

    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f'not authorize to perform action')
    
    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()

    return post_query.first()
