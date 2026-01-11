from typing import Generator
from app.core.database import get_db as _get_db

def get_db():
    """
    Dependency Injection for MongoDB Database.
    Wrapper around core.database.get_db to be used in API endpoints.
    Usage: db = Depends(get_db)
    """
    return _get_db()
