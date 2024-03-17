from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    id: int
    name: str
    age: int


DB: list[Person] = [
    Person(id=1, name='a', age=11),
    Person(id=2, name='b', age=12)
]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/db")
def read_item():
    return DB