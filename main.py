from typing import Optional
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel


app = FastAPI()


# all get operations here


@app.get("/")
def home():
    return {"data": "home page"}


@app.get("/blog")
def blogWrite(limit, published: bool):
    if published:
        return {"data": f"{limit} published blog write perfectly"}
    else:
        return {"data": f"{limit} blog write perfectly 12"}


@app.get("/{id}")
def index(id: int):
    return {"data": {"blogs here", id}}


@app.get("/show/{id}")
def show(id):
    return {"data ": {"1", "2"}}


class Blog(BaseModel):
    title: str
    author: str
    published: Optional[bool]
    price: int


# all post operation here


@app.post("/blog", response_class=PlainTextResponse)
def create_blog(blog: Blog):
    return (
        f"The blog title is {blog.title}.\n"
        f"The blog author is {blog.author}.\n"
        f"Which is price {blog.price}"
    )
