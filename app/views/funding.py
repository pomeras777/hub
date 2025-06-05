from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/fund_project/{project_id}")
def fund_get(request: Request, project_id: int):
    return templates.TemplateResponse("fund_project.html", {"request": request, "project_id": project_id})

@router.post("/fund_project/{project_id}")
def fund_post(request: Request, project_id: int, name: str = Form(...), amount: float = Form(...)):
    conn = sqlite3.connect("russhub.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS funding (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        name TEXT,
        amount REAL,
        donated_at TEXT
    )""")
    cursor.execute("""INSERT INTO funding (project_id, name, amount, donated_at)
                      VALUES (?, ?, ?, ?)""", (project_id, name, amount, datetime.utcnow().isoformat()))
    conn.commit()
    return RedirectResponse(f"/projects/{project_id}", status_code=303)

