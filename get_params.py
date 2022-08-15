#-*- coding:utf-8 -*-

from fastapi import FastAPI
from enum import Enum
from typing import Union

class ModelName(str, Enum):
    # 预选设定可能的有效参数值
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"



app = FastAPI()

@app.get("/") # 路径操作装饰器： 请求路径为  `/`，使用 get 操作
async def root()->dict:
    """ 位于装饰器下方的函数（也可以不使用 async）：
    当 FastApi 接收一个使用 get 方法访问 URL　`/` 的请求时，
    这个函数就会被调用
    :return: dict
    """
    # 默认： http://127.0.0.1:8000
    return {"message": "Hello World"}

@app.get("/items/{item_id}") # 路径参数 `item_id` 将作为参数，传给函数read_item
def read_item(item_id: int):
    # 尝试一下访问 http://127.0.0.1:8000/items/3
    return {"item_id": item_id}

@app.get("/users/me") # 路径操作是按顺序执行的
def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "leCNN all the image"}
    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}") # 传入路径参数需要加 :path的说明
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# 声明不属于路径参数的其他函数参数时，它们将被自动解释为 “查询字符串” 参数
@app.get("/items/")
async def read_item(skip: int=0, limit: int=10):
    """ 查询字符串是 键值对的集合，这些键值对位于 URL的 `?` 之后，并以 `&` 符号分割
    例如，访问如下url：http://127.0.0.1:8000/items/?skip=0&limit=10
    """
    return fake_items_db[skip: skip+limit]

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None]=None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# 查询参数类型转换
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None]=None, short: bool=False):
    """ 尝试访问以下URL：
    http://127.0.0.1:8000/items/foo?short=1
    http://127.0.0.1:8000/items/foo?short=True
    http://127.0.0.1:8000/items/foo?short=true
    http://127.0.0.1:8000/items/foo?short=on
    http://127.0.0.1:8000/items/foo?short=yes
    函数接收的 short 参数 都会是 True
    """
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


