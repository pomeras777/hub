from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.views import auth, home, projects
from app.views import profile
from app.views import funding


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
app.include_router(home.router)
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(profile.router)
app.include_router(funding.router)

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


