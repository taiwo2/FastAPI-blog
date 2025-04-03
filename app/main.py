from fastapi import FastAPI
from app.controllers import auth_controller, post_controller
from app.database import Base, engine
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Blog API",
    description="A simple blog API with authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_controller.router, prefix="/auth", tags=["Authentication"])
app.include_router(post_controller.router, prefix="", tags=["Posts"])

@app.get("/")
def read_root():
    """
    Root endpoint that returns a simple message.
    """
    return {"message": "Welcome to the Blog API"}