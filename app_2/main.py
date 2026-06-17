from typing import Optional

from fastapi import FastAPI, status, HTTPException, Depends, APIRouter, Response
from datetime import date
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# for 
# sqlalchemy
from . import models, schemas, utils, oauth2
from app_2.database import engine, Base, get_db
from sqlalchemy import and_
from sqlalchemy.orm import Session
import bcrypt

#security 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


app_2 = FastAPI()  #FastAPI object

models.Base.metadata.create_all(bind=engine)  # Create all tables in database from ORM models

class Students(BaseModel):
    Roll_No :  Optional[int] = None
    Name : str
    Std :  Optional[str] = None 
    # Gender : str
    DOB : date 
    Subject : str
    House : str
    
class Update_Students(BaseModel):
    Roll_No :  Optional[int] = None
    Name : Optional[str] = None
    Std :  Optional[str] = None 
    DOB : Optional[date] = None 
    Subject : Optional[str] = None
    House : Optional[str] = None
    
try:
    conn = psycopg2.connect(
        host='localhost',
        port='5433',  
        database='fastapi',
        user='postgres',
        password='postgres',
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("Database Connected Successfully!!")

except Exception as error:
    print("Connecting to database failed")
    print("Error:", error)
    time.sleep(2)
    
# @app_2.get("/student1")
# def root():
#     cursor.execute("SELECT * FROM students")
#     stud1 = cursor.fetchall()
#     print(stud1)
#     return {"data" : stud1}

# @app_2.get("/student2/{Std}/{Subject}")
# def root(Std : str, Subject : str):
#     cursor.execute("""SELECT "Roll_No", "Name" , "Std" , "Subject" FROM students WHERE "Std" = %s AND "Subject" = %s""",(Std,Subject))
#     stud2 = cursor.fetchall()
#     print(stud2)
#     return {"data": stud2}

# @app_2.post("/student3", status_code= status.HTTP_201_CREATED)
# def root(stud : Students):
#     cursor.execute("""INSERT INTO students("Name","DOB","Subject","House") VALUES (%s,%s,%s,%s) RETURNING * """, (stud.Name, stud.DOB, stud.Subject, stud.House))
#     stud3 = cursor.fetchone()
#     conn.commit()
#     return {"data" : stud3} 

# @app_2.put("/student4/{Roll_No}")
# def root(Roll_No : int, stud : Students):
#     cursor.execute("""UPDATE students SET "Subject" = %s WHERE "Roll_No" = %s RETURNING * """,(stud.Subject, Roll_No))
#     stud4 = cursor.fetchone()
#     conn.commit()
#     return {"data": stud4}

# @app_2.delete("/student5/{Roll_No}", status_code= status.HTTP_204_NO_CONTENT)
# def root(Roll_No: int):
#     cursor.execute("""DELETE FROM students WHERE "Roll_No" = %s RETURNING * """,(Roll_No,))
    
#     stud5 = cursor.fetchone()
#     conn.commit()
#     if stud5 == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with Roll_No {Roll_No} not found")
    
#     return {"data": stud5}

# @app_2.patch("/student6/{Roll_No}")
# def root(Roll_No: int, stud: Update_Students):
    
#     if stud.Name is not None:
#         cursor.execute("""UPDATE students SET "Name" = %s  WHERE "Roll_No" = %s RETURNING * """,(stud.Name, Roll_No))
        
#     if stud.Std is not None:
#         cursor.execute("""UPDATE students SET "Std" = %s WHERE "Roll_No" = %s RETURNING * """,(stud.Std, Roll_No))
        
#     if stud.DOB is not None:
#         cursor.execute("""UPDATE students SET "DOB" = %s WHERE "Roll_No" = %s RETURNING * """,(stud.DOB, Roll_No))
        
#     if stud.Subject is not None:
#         cursor.execute("""UPDATE students SET "Subject" = %s WHERE "Roll_No" = %s RETURNING * """,(stud.Subject, Roll_No))

#     if stud.House is not None:
#         cursor.execute("""UPDATE students SET "House" = %s WHERE "Roll_No" = %s RETURNING * """,(stud.House, Roll_No))
        
#     conn.commit()
#     cursor.execute("""SELECT * FROM students WHERE "Roll_No" = %s""",(Roll_No,)) 
#     update_std = cursor.fetchone()
#     return {"data" : update_std}       



# @app_2.get("/student7",response_model=list[schemas.Response_Students])
# def root(db : Session = Depends(get_db)):
#     s = db.query(models.Std).all()  #select * from students
#     return s

# @app_2.get("/student8/{Std}", response_model=list[schemas.Response_Students])
# def root(Std: str, db : Session = Depends(get_db)):
#     s = db.query(models.Std).filter(models.Std.Std == Std).all()
#     return s

# @app_2.get("/student9/{Roll_No}", responce_model = schemas.Response_Students)
# def root(Roll_No : int, db : Session = Depends(get_db)):
#     s = db.query(models.Std).filter(models.Std.Roll_No == Roll_No).first()
#     return {"data" : s}
    
# @app_2.get("/student10/{Roll_No}/{Std}",responce_model = schemas.Response_Students)
# def root(Roll_No : int, Std : str, db : Session = Depends(get_db)):
#     s = db.query(models.Std).filter(and_(models.Std.Roll_No == Roll_No, models.Std.Std == Std)).all()
#     return {"data" : s}

# @app_2.post("/student11", response_model=schemas.Response_Students, status_code= status.HTTP_201_CREATED)
# def root(stud : schemas.Create_Students, db: Session = Depends(get_db)):
#     s = models.Std(
#         # Roll_No = stud.Roll_No,
#         Name = stud.Name,
#         Std = stud.Std,
#         DOB = stud.DOB,
#         Subject = stud.Subject,
#         House = stud.House
#     )
#     db.add(s)
#     db.commit()
#     db.refresh(s)
#     return {"msg": "Student Data added", "Roll_No" : s.Roll_No}

# @app_2.post("/student12",response_model= schemas.Response_Students, status_code= status.HTTP_201_CREATED)  #response_model hides unwanted fields automatically.
# def root(stud: schemas.Create_Students, db: Session = Depends(get_db)):   #validates incoming request body.
#     s = models.Std(**stud.dict())
#     db.add(s)
#     db.commit()
#     db.refresh(s)
#     return s


# @app_2.put("/student13/{Roll_No}")
# def root(Roll_No : int, stud: schemas.Update_Students, db: Session = Depends(get_db)):
#     s = db.query(models.Std).filter(models.Std.Roll_No == Roll_No).first()
#     if s is None:
#         return {"msg": "Student not found"}
    
#     s.Name = stud.Name
#     s.Std = stud.Std
#     s.DOB = stud.DOB
#     s.Subject = stud.Subject
#     s.House = stud.House

#     db.commit()
#     db.refresh(s)
#     return {"data" : s}

# @app_2.put("/student14/{Roll_No}")
# def root(Roll_No : int, stud: schemas.Update_Students, db : Session = Depends(get_db)):
#     s = db.query(models.Std).filter(models.Std.Roll_No == Roll_No).first()
#     if not s:
#         return {"msg":"Student not found"}
    
#     s.Name = stud.Name
#     s.Std = stud.Std
#     s.DOB = stud.DOB
#     s.Subject = stud.Subject
#     s.House = stud.House
    
#     db.commit()
#     db.refresh(s)
#     return s


# @app_2.delete("/student15/{Roll_No}")
# def root(Roll_No: int, db: Session = Depends(get_db)):
#     s = db.query(models.Std).filter(models.Std.Roll_No == Roll_No)
#     if s.first() is None:
#         return {"msg" : "Student not found"}
#     s.delete(synchronize_session= False)
#     db.commit()
#     return {"msg" : "Student Deleted"}

# @app_2.delete("/student16/{Roll_No}")
# def root(Roll_No: int, db: Session = Depends(get_db)):
#     s = db.query(models.Std).filter(models.Std.Roll_No == Roll_No).first()
#     if s is None:
#         return{"msg" : "Student not exist"}
#     db.delete(s)
#     db.commit()
#     return {"msg" : s}


# @app_2.patch("/student17/{Roll_No}")
# def root(Roll_No: int, stud : schemas.Update_Students, db: Session = Depends(get_db)):
#     s = db.query(models.Std).filter(models.Std.Roll_No == Roll_No).first()
#     if s is None:
#         return{"msg": "Student not exist"}
    
#     update_data = stud.dict(exclude_unset= True)
    
#     for key, value in update_data.items():
#         setattr(s, key, value) #ORM object
        
#     db.commit()
#     db.refresh(s)
#     return s

# user Lohin and Logout
# @app_2.get("/login1") #Get all users from Login table
# def root(db: Session = Depends(get_db)):
#     l = db.query(models.Login).all()
#     return {"data" : l}

# # Get a single user by ID
# @app_2.get("/login4/{id}", response_model= schemas.User_Logout)
# def root(id : int, db : Session = Depends(get_db)):
#     l = db.query(models.Login).filter(models.Login.id == id).first()
#     if not l:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} don't exist")
#     return l

# # Create a new user (password stored as plain text - NOT recommended)
# @app_2.post("/login2", status_code= status.HTTP_201_CREATED)
# def root(log : schemas.Create_Login, db : Session = Depends(get_db)):
#     l =  models.Login(**log.dict())    
#     db.add(l)
#     db.commit()
#     db.refresh(l)
#     return l
 
# # Create a new user with hashed password (recommended)   
# @app_2.post("/login3", status_code= status.HTTP_201_CREATED, response_model= schemas.User_Logout)   #this schema show on output 
# def root(log : schemas.Create_Login, db : Session = Depends(get_db)):      #this schema show in json boby 
    
#     #hash the password - log.password 
#     hashes_password = utils.hash(log.password)
#     log.password = hashes_password
    
#     l = models.Login(**log.dict())
#     db.add(l)
#     db.commit()
#     db.refresh(l)
#     return l   

# #user authentication

# # Authenticate user (login)
# # Verify email and password
# # Generate and return JWT access token
# @app_2.post("/auth1")
# # def root(auth : schemas.User_Auth, db: Session = Depends(get_db)):
# def root(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
#     a = db.query(models.Login).filter(models.Login.email == user_credentials.username).first()
#     if not a:
#         raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Invalid cendentials")
    
#     if not utils.verify(user_credentials.password, a.password):
#         raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Invalid Credentials")
    
#     #create a token
#     #return token
#     access_token = oauth2.create_access_token(data = {"user_id" : a.id})
#     return {"access_token" : access_token, "token_type" : "bearer"}

# # Protected route
# # Requires a valid JWT token
# # Creates a new user only if the requester is authenticated
# @app_2.post("/auth2", status_code= status.HTTP_201_CREATED, response_model= schemas.User_Logout)   #this schema show on output 
# def root(log : schemas.Create_Login, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):      #this schema show in json boby 
    
#     #hash the password - log.password 
#     hashes_password = utils.hash(log.password)
#     log.password = hashes_password
    
#     print(current_user.email)
#     l = models.Login(**log.dict())
#     db.add(l)
#     db.commit()
#     db.refresh(l)
#     return l 




 
 