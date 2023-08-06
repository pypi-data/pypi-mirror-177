from typing import Optional

import uvicorn
from fastapi import FastAPI

from simple_test_packet.config import redis_connect
from simple_test_packet.models import Item

app = FastAPI()
client = redis_connect()


@app.get("/")
def read_root(name: Optional[str] = None):
    return {"Hello": name}


@app.get("/redis")
def get_redis_key(key: Optional[str] = None):
    if key:
        value = client.get(key)
        return {key: value}
    return 'Укажите ?key='


@app.post("/name")
def create_item(item: Item):
    return item


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("simple_test_packet.main:app", host="0.0.0.0", port=8080, reload=True)
