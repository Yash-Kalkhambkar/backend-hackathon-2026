# Database connection setup using SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine with SSL requirement for cloud database
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"sslmode": "require"}
)

# Create session factory for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


# Dependency to get database session for each request
def get_db():
    """Provide a database session for each request and close it after"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables if they don't exist (checkfirst=True prevents errors if table exists)
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine, checkfirst=True)
