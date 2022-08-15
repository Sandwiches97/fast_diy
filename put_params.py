#-*- coding:utf-8 -*-

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    # 同时声明请求体、路径参数和查询参数
    return {"item_id": item_id, **item.dict()}

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None]=None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

