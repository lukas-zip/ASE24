from typing import Union
from fastapi import FastAPI

app = FastAPI()

class Person(BaseModel):
    id: int
    name: str
    age: int


DB: list[Person] = [
    Person(id=1, name='a', age=11),
    Person(id=2, name='b', age=12)
]


@app.get("/company/{company_id}")
def read_root():
    return 'company retrieved successfully' 


@app.delete("/company/{company_id}")
def delete_item(item_id: int, q: Union[str, None] = None):
    return 'company deleted successfully' 


@app.put("/company/{company_id}")
def update_item():
    return 'company updated successfully'

@app.post("/company/{company_id}")
def add_item():
    return 'company added successfully'


##################

@app.get("/user/{company_id}")
def read_root():
    return 'user retrieved successfully' 


@app.delete("/user/{company_id}")
def delete_item(item_id: int, q: Union[str, None] = None):
    return 'user deleted successfully' 


@app.put("/user/{company_id}")
def update_item():
    return 'user updated successfully'

@app.post("/user/{company_id}")
def add_item():
    return 'user added successfully'