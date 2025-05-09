from typing import Union

from fastapi import FastAPI
import firebase_admin

app = FastAPI()
default_app = firebase_admin.initialize_app()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
