from fastapi import FastAPI, Form, Request
from typing import Union, Dict
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")
memos = dict()
idTop = 0
memos[idTop] = 'TestMemo12345' #테스트 용
idTop += 1


@app.get("/")
def root():
    return "Hello World"

@app.get("/name", response_class=HTMLResponse)
def read_name(request:Request):
    return templates.TemplateResponse("name.html", {"request":request})

@app.post("/name", response_class=HTMLResponse)
def read_name(request:Request, name: str = Form(...)):
    return templates.TemplateResponse("post_name.html", {"request":request, "name":name})

@app.get("/memo") #CRUD중 Read에 해당합니다.
def read_memos_page(request:Request):
    return templates.TemplateResponse("memo.html", {"request":request, "memos":memos})

@app.get("/memoupdate/{id}") #CRUD중 Update에 해당합니다.
def update_memo_page(request:Request, id:int):
    memo = memos[id]
    return templates.TemplateResponse("memoupdate.html", {"request":request, "id":id, "memo" : memo})

@app.post("/memoupdate/{id}")
def update_memo(id:int, memo:str=Form(...)):
    if(id in memos):
        memos[id] = memo
        return "Done"
    else:
        return "Fail"

@app.get("/memocreate") #CRUD중 Create에 해당합니다.
def create_memo_page(request:Request):
    return templates.TemplateResponse("memocreate.html", {"request":request})

@app.post("/memocreate")
def create_memo(memo:str=Form(...)):
    global idTop
    try:
        memos[idTop] = memo
        idTop += 1
        return "Done"
    except Exception as e:
        return str(e)
    
@app.get("/memodelete/{id}") #CRUD중 Delete에 해당합니다.
def create_memo(request:Request, id:int):
    try:
        del memos[id]
        return templates.TemplateResponse("memodelete.html", {"request":request, "response" : "Done"})
    except:
        return templates.TemplateResponse("memodelete.html", {"request":request, "response" : "Fail"})
    
@app.get("/jsontest")
def test_json(request:Request):
    return templates.TemplateResponse("jsontest.html", {"request":request})

class TestJsonData(BaseModel):
    name:str
    sid:str
    gpa1:str
    gpa2:str

@app.post("/jsontest")
def test_json(data: TestJsonData):
    return {"message":"Done", "avgGpa" : str(round((float(data.gpa1)+float(data.gpa2))/2,2))}