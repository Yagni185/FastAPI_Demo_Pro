from datetime import  datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint

# Data client sends
# class Create_Students(BaseModel):

#     Name : str
#     Std :  Optional[str] = None 
#     # Gender : str
#     DOB : date 
#     Subject : str
#     House : str

# Data API returns
# class Response_Students(BaseModel):
#     Roll_No : int  #Because response always contains database-generated ID.
#     Name : str
#     Std :  Optional[str] = None
#     DOB : date
#     Subject : str
#     House : str
    
#     class Config:
#         orm_mode = True
        
# Partial update fields
# class Update_Students(BaseModel):
#     Name : Optional[str] = None
#     Std :  Optional[str] = None 
#     DOB : Optional[date] = None 
#     Subject : Optional[str] = None
#     House : Optional[str] = None
    
# class Create_Login(BaseModel):
#     email : EmailStr
#     password : str
    
#     class Config: 
#         orm_mode = True
        
# class User_Logout(BaseModel):
#     id : int
#     email : EmailStr
    
#     class Config: 
#         orm_mode = True
        
class User_Auth(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel): 
    id: int | None= None
 
#For User1 and User2        
class Create_User1(BaseModel):
    email : EmailStr
    password : str 
    post_id : int
    
    class Config:
        orm_mode = True
    
class Create_User2(BaseModel):
    post_type : str
    id_type : bool
    
    class Config:
        orm_mode = True

class Response_User2(BaseModel):
    id : int
    post_type : str
    id_type : bool
    created_time : datetime
    
    class Config:
        orm_mode = True
             
             
class Response_User1(BaseModel):
    id : int
    email : EmailStr
    post_id : int
    user1 : Response_User2
    
    class Config:
        orm_mode = True
        
class Update_User1(BaseModel):
    email : Optional[EmailStr] = None
    password : Optional[str] = None
    post_id : Optional[int] = None
    
class Update_User2(BaseModel):
    post_type : Optional[str] = None
    id_type : Optional[str] = None
    
#for voting
class Vote(BaseModel):
    post_id : int
    dir: conint(le=1) #le means less than or equal to 1, so dir can only be 0 or 1
    
class Response_of_user1(BaseModel):
    id : int
    email : EmailStr
    
    class Config:
        orm_mode = True
        
class UserVoteCount(BaseModel):
    User1: Response_User1
    votes: int

    class Config:
        orm_mode = True
        