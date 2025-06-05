from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import sqlite3

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home(request: Request):
    conn = sqlite3.connect("russhub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description FROM projects ORDER BY created_at DESC")
    projects = cursor.fetchall()
    return templates.TemplateResponse("home.html", {"request": request, "projects": projects})
