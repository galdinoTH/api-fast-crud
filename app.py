from fastapi import FastAPI, HTTPException, status, Query, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange

from data import my_list

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None


@app.get("/posts")
def get_all_posts():
    return {"data": my_list}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_list.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_list[-1]
    return {"post_detail": post}


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} does not exist")
    my_list.pop(index)
    return {"message": f"Post with ID {id} successfully deleted"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_list[index] = post_dict
    return {"message": f"Post with ID {id} successfully updated"}


def find_post(id):
    for p in my_list:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_list):
        if p['id'] == id:
            return i


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"message": "api-health-check", "status": 200, }
