import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
# All SQL models must be imported here so Base.metadata is fully populated
from models.sql import Base, User, UserLockConfiguration  # noqa: F401


def _get_engine():
    """Build the engine lazily so load_dotenv() in main.py runs first."""
    url = os.getenv(
        "DATABASE_URL",
        "postgresql://puryfi:puryfi@localhost:5432/puryfi_chaster",
    )
    return create_engine(url, echo=False)


engine = None
SessionLocal = None


def _ensure_engine():
    global engine, SessionLocal
    if engine is None:
        engine = _get_engine()
        SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db() -> None:
    """Create all tables that do not yet exist. Safe to call on every startup."""
    _ensure_engine()
    print(f"[DB] Connecting to: {engine.url}")
    inspector = inspect(engine)
    existing = inspector.get_table_names()

    missing = [
        table
        for table in Base.metadata.tables
        if table not in existing
    ]

    print(f"[DB] Known models: {list(Base.metadata.tables.keys())}")

    if missing:
        print(f"[DB] Creating missing tables: {missing}")
        Base.metadata.create_all(engine)
    else:
        print("[DB] All tables already exist, skipping creation.")


def get_db() -> Session:
    """Dependency for FastAPI routes: yields a DB session and closes it after use."""
    _ensure_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
