from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import analyze, health
from src.utils.config import load_settings

settings = load_settings()

app = FastAPI(
    title="SkillScope API",
    description="Skill gap analysis between resumes and job descriptions.",
    version="1.0.0",
)

# Root route (ADD THIS)
@app.get("/")
def root():
    return {
        "message": "SkillScope API is running",
        "docs": "/docs",
        "health": "/health"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings["api"]["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(analyze.router, prefix="/api/v1", tags=["Analysis"])