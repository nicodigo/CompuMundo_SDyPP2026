from fastapi import FastAPI
from pydantic import BaseModel
from common.tarea import Tarea

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


# class Tarea(BaseModel):
#     a: int
#     b: int


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.put("/ejecutar_tarea/{tarea_id}")
def get_tarea_remota(tarea_id:int, tarea: Tarea):
    restl: int = tarea.a + tarea.b
    return {"tarea_id": tarea_id, "resultado": restl}
