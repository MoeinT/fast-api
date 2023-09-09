from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Item

app = FastAPI()
templates = Jinja2Templates(directory="../templates")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "items": items}
    )


@app.get("/items/{item_id}", response_class=HTMLResponse)
async def read_details(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        return templates.TemplateResponse(
            "index_details.html", {"request": request, "item": item}
        )
    print(f"Item {item_id} not found!")
