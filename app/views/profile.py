from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import sqlite3

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/profile/{username}")
def user_profile(request: Request, username: str):
    conn = sqlite3.connect("russhub.db")
    cursor = conn.cursor()

    # Получаем пользователя
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        return templates.TemplateResponse("profile.html", {"request": request, "error": "Пользователь не найден"})

    user_id = user[0]

    # Получаем его проекты
    cursor.execute("SELECT id, title, description FROM projects WHERE user_id = ?", (user_id,))
    projects = cursor.fetchall()

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "username": username,
        "projects": projects
    })
