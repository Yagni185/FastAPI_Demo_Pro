from fastapi import FastAPI,Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from typing import List

from . import models
from .database import engine, get_db 
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind = engine)
        
app = FastAPI()

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    s = db.query(models.Student).all()
    return {"data": s, "status": "success"}

# class Post(BaseModel):
#     title: str
#     content : str
#     published : bool = True
#     rating : Optional[int] = None

# while True:
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
    print("Database connection was successful")
    # break

except Exception as error:
    print("Connecting to database failed")
    print("Error:", error)
    time.sleep(2)

    
# my_post = [{"Name": "Python", "Roll_No": 1, "id": 101},{"Name": "Java", "Roll_No": 2, "id": 102},{"Name": "C", "Roll_No": 3, "id": 103}]
# # print(my_post)


# def find_post(id):
#     for i in my_post:
#         if i["id"] == id:
#             return i
        
# def find_index_post(id):
#     for i,j in enumerate(my_post):
#         if j['id'] == id:
#             return i
#     return None #explicitly return None

    
# # request  get method url: "/"
# @app.get("/")
# def root():
#     return {"message": "Hello World"}

# # @app.get("/posts")
# # def get_posts():
# #     return {"data": my_post}

# @app.get("/post_sql")
# def root():
#     # cursor.execute("""SELECT title,content FROM posts""")
#     cursor.execute("""SELECT * FROM posts""")
#     postA = cursor.fetchall()
#     print(postA)
#     return {"data": postA}

# @app.get("/post_sql2/{id}/{title}")
# def root(id: int, title: str):
#     # cursor.execute("""SELECT title,content,published FROM posts WHERE id = %s""",(id,))
#     cursor.execute("""SELECT title,content,published FROM posts WHERE id = %s AND title = %s""",(id, title))
#     postB = cursor.fetchone()
#     print(postB)
    
#     if not postB:
#         raise HTTPException(status_code=404, detail="Post not found")
    
#     return postB

# @app.post("/post_sql3", status_code= status.HTTP_201_CREATED)
# def root(postsq : Post):
#     cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """,(postsq.title,postsq.content,postsq.published))
#     postC = cursor.fetchone()
#     conn.commit()
#     return {"data" : "new_post"}
#     # return {"data" : "created post"}


# @app.get("/get_method")
# def root():
#     return {"message": "Hello from API creation"}

# @app.post("/add_title")
# def post_root(payload: dict = Body(...)):
#     print("---inside---")
#     return{"new_post": f"title: {payload['title']} content: {payload['content']}"}

# @app.post("/new_post")
# def new_post(post: Post):
#     # print(post)
#     # print(post.dict())
    
#     post_dict = post.dict()
#     post_dict["Roll_No"] = randrange(0,100000)
#     my_post.append(post_dict)
#     return{"data" : post_dict}

# @app.get("/post1/{id}")
# def get_post1(id : int):  #covert string id to int id
#     # print(type(id))
#     post = find_post(id)
#     print(post)
#     return {"post_details":post}


# @app.get("/post2/latest")
# def get_latest_post():
#     post = my_post[len(my_post)-1]
#     return {"detail": post}

# @app.get("/post3/{id}")
# def get_response(id: int):   #, response : Response
#     post = find_post(id)
#     if not post:
#         # response.status_code = 404
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'msg': f"post with id: {id} was not found"}
        
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
#                             detail= f"post with id: {id} was not found")
#     return {"post_detail": post}


# @app.delete("/post/{id}")
# def delete_post(id: int):
#     index = find_index_post(id)
    
#     if index is None:
#         raise HTTPException(status_code= 404, detail="Post Not found")
#     my_post.pop(index)
#     return {'msg':f'post {id} was successfully deleted'}


# @app.put("/post5/{id}")
# def update_post(id: int, post: Post):
#     # print(post)
#     index = find_index_post(id)
    
#     if index == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} don't exist")
    
#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_post[index] = post_dict
#     return {"data": post_dict}


# @app.post("/post_sql4")
# def root(post_sq : List[Post]):
#     post_list = [(i.title, i.content) for i in post_sq]
#     cursor.executemany("""INSERT INTO posts(title, content) VALUES (%s,%s)""", post_list)
#     conn.commit()
#     return {"msg" : "Multiple values inserted"}

# @app.delete("/post_sql5/{id}", status_code= status.HTTP_204_NO_CONTENT)
# def root(id : int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(id,))
#     delete_post = cursor.fetchone()
#     conn.commit()
    
#     if delete_post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} don't exist")
    
#     return {"data" : delete_post}

# @app.put("/post_sql6/{id}")
# def root(id : int, post : Post):
#     cursor.execute("""UPDATE posts SET published = %s WHERE id = %s  RETURNING * """, (post.published, id))
#     update_post = cursor.fetchone()
#     conn.commit()
#     return {"data": update_post}


# class Update_post(BaseModel):
#     title : Optional[str] = None
#     content: Optional[str] = None
#     published: Optional[bool] = None
    
# @app.patch("/patch_sql/{id}")
# def root(id : int, post : Update_post):
    
#     if post.title is not None:
#         cursor.execute("""UPDATE posts SET title = %s WHERE id = %s RETURNING""",(post.title, id))
    
#     if post.content is not None:
#         cursor.execute("""UPDATE posts SET content = %s where id = %s RETURNING * """, (post.content, id))
    
#     if post.published is not None:
#         cursor.execute("""UPDATE posts SET published = %s WHERE id = %s RETURNING * """, (post.published, id))

#     conn.commit()
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
#     update_data = cursor.fetchone()
#     return {"data": update_data} 