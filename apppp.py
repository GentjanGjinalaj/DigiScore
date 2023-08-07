from fastapi import FastAPI, Form, HTTPException
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root():
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def process_form(user_input: str = Form(...), competitor1: str = Form(None), ...):
    # Your processing logic here
