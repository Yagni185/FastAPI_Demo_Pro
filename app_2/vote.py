from fastapi import APIRouter, status, HTTPException, Depends, APIRouter, Response
from . import models, schemas, utils, oauth2
from app_2.database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/vote",
    tags = ['Vote']
)

@router.post("/vote1", status_code= status.HTTP_201_CREATED)
def root(vote: schemas.Vote, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user1)):
    
    post = db.query(models.User2).filter(models.User2.id == vote.post_id).first()
     
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id {vote.post_id} don't exist")
    
    vote_query = db. query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has always voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message" : "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "vote don't exist")
        vote_query.delete(synchronize_session = False)
        db.commit()
        
        return {"message" : "successfully deleted vote"}