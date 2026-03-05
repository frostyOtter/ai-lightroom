from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health
from app.config import settings

app = FastAPI(
    title="AI Lightroom API",
    description="AI-powered image color adjustment API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])


@app.get("/")
async def root():
    return {"message": "AI Lightroom API", "version": "1.0.0", "status": "running"}


@app.on_event("startup")
async def startup_event():
    print("🚀 AI Lightroom API starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    print("👋 AI Lightroom API shutting down...")
