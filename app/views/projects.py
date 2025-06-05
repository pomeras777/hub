from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import os, shutil, sqlite3
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "media/"

@router.get("/upload")
def upload_get(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@router.post("/upload")
def upload_post(request: Request,
                title: str = Form(...),
                description: str = Form(...),
                file: UploadFile = File(...)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    conn = sqlite3.connect("russhub.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projects (title, description, user_id, created_at, file_path) VALUES (?, ?, ?, ?, ?)",
                   (title, description, user_id, datetime.utcnow().isoformat(), file_path))
    conn.commit()
    return RedirectResponse(url="/", status_code=303)

@router.get("/projects/{project_id}")
def project_detail(request: Request, project_id: int):
    conn = sqlite3.connect("russhub.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.title, p.description, p.file_path, u.username
        FROM projects p JOIN users u ON p.user_id = u.id
        WHERE p.id = ?
    """, (project_id,))
    row = cursor.fetchone()
    if not row:
        return templates.TemplateResponse("project_detail.html", {"request": request, "error": "Проект не найден"})

    title, description, file_path, username = row
    return templates.TemplateResponse("project_detail.html", {
        "request": request,
        "title": title,
        "description": description,
        "file_path": file_path,
        "username": username
    })
