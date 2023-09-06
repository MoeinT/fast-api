from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="../templates")

# Define a list of items (for demonstration purposes)
items = [
    {"id": 1, "name": "Item 1", "description": "Description of Item 1"},
    {"id": 2, "name": "Item 2", "description": "Description of Item 2"},
    {"id": 3, "name": "Item 3", "description": "Description of Item 3"},
]

# Home page containing all items
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

# Route logic for each item
@app.get("/item/{item_id}", response_class=HTMLResponse)
async def read_detail(request: Request, item_id: int):

    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return templates.TemplateResponse("index_details.html", {"request": request, "item": item})
    print(f"Item {item_id} not found!")