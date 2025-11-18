from typing import Generator
from sqlalchemy.orm import Session
from database import SessionLocal

def get_db() -> Generator:
    """
    Dependency that provides a database session.
    Ensures the session is properly closed after the request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
