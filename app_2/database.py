from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import setting

Sql_Database_URL = f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}'
# print(Sql_Database_URL)
engine = create_engine(Sql_Database_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()

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
    print("Databsae Successfully Connected")

except Exception as error:
    print("Connecting to database failed")
    print("Error:", error)
    time.sleep(2)
        
        
        