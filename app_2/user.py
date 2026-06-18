from fastapi import FastAPI, status, HTTPException, Depends, APIRouter, Response
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas, utils, oauth2, vote
from app_2.database import engine, Base, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
import bcrypt
from typing import List, Optional
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

app_2 = FastAPI()

origins = ["*"]

#router 
app_2.include_router(vote.router)

models.Base.metadata.create_all(bind=engine)  # Create all tables in database from ORM models

app_2.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

  
@app_2.post('/user1', status_code = status.HTTP_201_CREATED, response_model= schemas.Response_User1)
def root(user: schemas.Create_User1, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user1)):
    
    hashes_password = utils.hash(user.password)
    user.password = hashes_password
    
    person = models.User1(**user.dict())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person

@app_2.post('/user2', status_code= status.HTTP_201_CREATED, response_model= schemas.Response_User2)
def root(user: schemas.Create_User2, db : Session = Depends(get_db)):
    
    person = models.User2(**user.dict())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person

@app_2.get('/user3',response_model= List[schemas.Response_User1])
def root(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user1), Limit : int = 9):
    print(Limit)
    #using slicing
    person = db.query(models.User1).limit(Limit).all()

    return person
    # return users[:limit]

@app_2.get('/user8', response_model= List[schemas.Response_User1])
def root(db : Session = Depends(get_db),search : Optional[str] = ""): 
    # person = db.query(models.User1).limit(4).all()
    # person = db.query(models.User1).offset(2).all()
    person = db.query(models.User1).filter(models.User1.email.contains(search)).offset(2).limit(8).all()
    return person

@app_2.get('/user7', response_model= List[schemas.Response_User1])
def root( db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user1)):
    person = db.query(models.User1).filter(models.User1.id == current_user.id).all()
    # print(person)
    return person

@app_2.get('/user4')
def root(db: Session = Depends(get_db)):
    person = db.query(models.User2).all()
    return {"data" : person}

@app_2.get('/user11')
def root(db : Session = Depends(get_db)):
    person = db.query(models.User1).all()
    return {"data" : person}


#user authentication

# Authenticate user (User1)
# Verify email and password
# Generate and return JWT access token
@app_2.post("/authuser5")
# def root(auth : schemas.User_Auth, db: Session = Depends(get_db)):
def root(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    a = db.query(models.User1).filter(models.User1.email == user_credentials.username).first()
    if not a:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Invalid cendentials")
    
    if not utils.verify(user_credentials.password, a.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Invalid Credentials")
    
    #create a token
    #return token
    access_token = oauth2.create_access_token(data = {"user_id" : a.id})
    return {"access_token" : access_token, "token_type" : "bearer"}

# Protected route
# Requires a valid JWT token
# Creates a new user only if the requester is authenticated
@app_2.post("/authuser6", status_code= status.HTTP_201_CREATED, response_model= schemas.Response_User1)   #this schema show on output 
def root(user: schemas.Create_User1, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user1)):      #this schema show in json boby 
    
    #hash the password - user.password 
    hashes_password = utils.hash(user.password)
    user.password = hashes_password
    
    print(current_user.email)
    l = models.User1(**user.dict())
    db.add(l)
    db.commit()
    db.refresh(l)
    return l 

@app_2.get('/user9', response_model= List[schemas.Response_User1])
def root(db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user1), search: Optional[str] = ""):
    # person = db.query(models.User1).filter(models.User1.email.contains(search)).limit(6).offset(2).all()
    # return person
    
    #left outer join
    result = db.query(models.User1).join(models.Vote, models.User1.id == models.Vote.user_id, isouter= True).filter(models.User1.email.contains(search)).all()
    # result = db.query(models.User1, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.user_id == models.User1.id, isouter= True).group_by(models.User1.id).all()
    # print(result)
    return result

@app_2.get('/user10', response_model=List[schemas.UserVoteCount])
def root(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user1)
):
    result = (
        db.query(
            models.User1,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(
            models.Vote,
            models.Vote.user_id == models.User1.id,
            isouter=True
        )
        .group_by(models.User1.id)
        .all()
    )

    return result
    
    
    
    
    