from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from backend.routes.game import router as game_router

load_dotenv()

app = FastAPI(
    title="Prompt And Theater",
    description="AI-powered medieval choose your own adventure",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(game_router, prefix="/api/game", tags=["game"])

@app.get("/")
async def root():
    from fastapi.requests import Request
    from fastapi.responses import HTMLResponse
    return templates.TemplateResponse("index.html", {"request": {}})

@app.on_event("startup")
async def startup_event():
    print("Prompt And Theater is running...")
    print(f"Visit: http://{os.getenv('APP_HOST', '127.0.0.1')}:{os.getenv('APP_PORT', '8000')}")