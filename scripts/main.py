from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="../templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})

@app.get("/about/", response_class=HTMLResponse)
async def about_root(request: Request):
    return templates.TemplateResponse(name="about.html", context={"request": request})

@app.get("/contact/", response_class=HTMLResponse)
async def contact_root(request: Request):
    return templates.TemplateResponse(name="contact.html", context={"request": request})