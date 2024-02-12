from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #will allow us to let people with different domains make requests
from random import randrange 
from app.schemas import *
from app.utils import *
import app.models as models
from app.models import *
from app.database import engine
from app.routers import user, post, auth, vote



#responsible for creating tables in 'models.py' by connecting with database using 'engine'
#this should only create tables that don't already exist

#models.Base.metadata.create_all(bind=engine) -- used to create tables without alembic

#uvicorn app.test:app --reload (first is the folder name, then the python file name, then finally the fast API instance)

app = FastAPI()

#origins will be a list including all domains allowed to make requests

origins = ["*"]

# if you want to set up a public api, you use  origins = ["*"]
# usually you'd only add the domain of your webapp

# middleware is basically a function that occurs before every request
# using allow_methods we can limit the requests other domains can make 

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

#routers connecting to the HTTP protocols belonging to each table

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def index():
    return {"Hello World"}

#ctrl + C to type things in terminal after using uvicorn

