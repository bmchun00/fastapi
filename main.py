from fastapi import FastAPI, Form, Request
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return "Hello World"

@app.get("/name", response_class=HTMLResponse)
def read_name(request:Request):
    return templates.TemplateResponse("name.html", {"request":request})

@app.post("/name", response_class=HTMLResponse)
def read_name(request:Request, name: str = Form(...)):
    return templates.TemplateResponse("post_name.html", {"request":request, "name":name})