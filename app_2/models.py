from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app_2.database import Base

class Std(Base):
    __tablename__ = 'students'

    Roll_No = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Name = Column(String, nullable=False)
    Std = Column(String, nullable= False, server_default= '12th')
    DOB = Column(Date, nullable= False)
    Subject = Column(String, nullable= False)
    House = Column(String, nullable= False)
      
class Login(Base):
    __tablename__ = 'login'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), nullable= False, server_default= text('now()'))   

# Foreign_Key
class User1(Base):
    __tablename__ = 'user1'
    
    id = Column(Integer, primary_key= True, autoincrement=True, nullable= False)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), nullable= False, server_default= text('now()'))
    post_id = Column(Integer, ForeignKey("user2.id", ondelete="CASCADE"), nullable= False)
    
    user1 = relationship("User2")
    
class User2(Base):
    __tablename__ = 'user2'
    
    id = Column(Integer, primary_key= True, autoincrement=True, nullable= False)
    post_type = Column(String, nullable= False)
    id_type = Column(Boolean, nullable= False)
    created_time = Column(TIMESTAMP(timezone= True), nullable= False, server_default= text('now()'))
    
class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey("user1.id", ondelete = "CASCADE"), primary_key = True)
    post_id = Column(Integer, ForeignKey("user2.id", ondelete = "CASCADE"), primary_key = True)
    


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)   