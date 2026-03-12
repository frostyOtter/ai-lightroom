from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 AI Lightroom API starting up...")
    yield
    print("👋 AI Lightroom API shutting down...")


app = FastAPI(
    title="AI Lightroom API",
    description="AI-powered image color adjustment API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])


@app.get("/")
async def root():
    return {"message": "AI Lightroom API", "version": "1.0.0", "status": "running"}
