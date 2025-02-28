import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import g, current_app

logger = logging.getLogger(__name__)
Base = declarative_base()

def get_engine():
    """Get SQLAlchemy engine from app config."""
    return create_engine(current_app.config["DATABASE_URI"])

def get_db():
    """Get or create database session."""
    if "db" not in g:
        engine = get_engine()
        session_factory = sessionmaker(bind=engine)
        g.db = scoped_session(session_factory)
    
    return g.db

def init_db():
    """Initialize database if needed."""
    # Only create tables in development/testing
    if current_app.config.get("TESTING") or current_app.config.get("DEBUG"):
        engine = get_engine()
        Base.metadata.create_all(engine)

def close_db(e=None):
    """Close database session at the end of request."""
    db = g.pop("db", None)
    
    if db is not None:
        db.close()
