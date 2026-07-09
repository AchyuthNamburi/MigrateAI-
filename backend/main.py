# backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
import logging

# Import routes
from backend.routes import auth, repositories

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Migration Agent",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ FIX: Mount static files - THIS IS CRITICAL FOR RENDER
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Templates
templates = Jinja2Templates(directory="frontend/templates")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(repositories.router, prefix="/api/repositories", tags=["Repositories"])

# ===== PAGE ROUTES =====
@app.get("/", response_class=HTMLResponse)
async def root():
    return {"message": "AI Migration Agent is running!"}

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

@app.on_event("startup")
async def startup():
    from backend.core.database import Base, engine
    from backend.models.user import User, UserProfile
    from backend.models.migration import MigrationJob, MigrationFile, MigrationReview, MigrationHistory
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")
