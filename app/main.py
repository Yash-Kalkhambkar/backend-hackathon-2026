# Main FastAPI application entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.escalation import router as escalation_router
from app.database import init_db

# Create FastAPI application instance
app = FastAPI(
    title="Escalation Detector API",
    description="API for detecting support conversation escalations using LLM",
    version="1.0.0"
)

# Configure CORS to allow frontend access from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables on startup
@app.on_event("startup")
def startup_event():
    """Initialize database tables when application starts"""
    init_db()

# Include escalation router with all endpoints
app.include_router(escalation_router)

# Root endpoint
@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Escalation Detector API",
        "docs": "/docs",
        "health": "/escalation/health"
    }
