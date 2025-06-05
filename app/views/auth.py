from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import hashlib

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

@router.get("/register")
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register_post(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect("russhub.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return RedirectResponse(url="/login", status_code=303)
    except sqlite3.IntegrityError:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Пользователь уже существует"})

@router.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect("russhub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = cursor.fetchone()
    if user:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie("user_id", str(user[0]))
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Неверные данные"})
