from sqlalchemy import Column, Integer, String
# from sqlalchemy.sql.expression import null
from .database import Base

class Student(Base):
    __tablename__ = 'std'
    
    id = Column(Integer, primary_key= True, nullable= False)
    name = Column(String, nullable= False)
    subject = Column(String, nullable= False, server_default = 'PCM')
    
    
    