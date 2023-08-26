from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

class ItemResponse(BaseModel):
    item_id: int
    item: Item

@app.post("/items/", response_model=ItemResponse)
def create_item(item: Item):
    return {"item_id": 1, "item": item}
