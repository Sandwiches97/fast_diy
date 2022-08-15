#-*- coding:utf-8 -*-

"""
当你需要将数据从客户端（例如浏览器）发送给 API 时，你将其作为「请求体」发送。

请求体是客户端发送给 API 的数据。响应体是 API 发送给客户端的数据。

你的 API 几乎总是要发送响应体。但是客户端并不总是需要发送请求体。

我们使用 Pydantic 模型来声明请求体，并能够获得它们所具有的所有能力和优点。
"""

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel): # 声明请求体，默认将其作为 JSON 读取
    name: str
    description: Union[str, None] = None  # 将默认值设为None，可使其成为可选属性
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):  # 声明了item的类型，
                                    # 你将可以在函数内部访问对象的所有属性
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


