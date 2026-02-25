import os
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///todo_app.db")

# Check if using SQLite
IS_SQLITE = DATABASE_URL.startswith("sqlite://")

# For Neon/Cloud databases, we need to handle SSL differently
# Convert regular postgresql:// to postgresql+asyncpg:// for async engine
def parse_database_url(url: str) -> tuple[str, dict]:
    """
    Parse database URL and extract SSL settings for asyncpg
    Returns (clean_url, connect_args)
    """
    connect_args = {}
    
    # SQLite doesn't need asyncpg
    if url.startswith("sqlite://"):
        return url, connect_args
    
    # Ensure we're using asyncpg for async operations
    if not url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://")
        if not url.startswith("postgresql+asyncpg://"):
            url = "postgresql+asyncpg://" + url.lstrip("postgresql://")
    
    # Handle SSL mode for Neon/cloud databases
    if "?sslmode=require" in url:
        url = url.replace("?sslmode=require", "")
        connect_args = {"ssl": "require"}
    elif "?ssl=true" in url:
        url = url.replace("?ssl=true", "")
        connect_args = {"ssl": "require"}

    return url, connect_args

async_database_url, connect_args = parse_database_url(DATABASE_URL)

# Create async engine (only for PostgreSQL)
if not IS_SQLITE:
    async_engine = create_async_engine(
        async_database_url,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args=connect_args,
    )
else:
    async_engine = None

# Create sync engine for non-async operations
if IS_SQLITE:
    # SQLite uses regular engine
    sync_engine = create_engine(
        async_database_url,
        echo=False,
        pool_pre_ping=True,
        connect_args=connect_args,
    )
else:
    # PostgreSQL: replace asyncpg with psycopg2
    SYNC_DATABASE_URL = async_database_url.replace("postgresql+asyncpg://", "postgresql://")
    sync_clean_url, _ = parse_database_url(SYNC_DATABASE_URL)
    sync_engine = create_engine(
        sync_clean_url,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=300,
    )

# Async session maker (only for PostgreSQL)
if not IS_SQLITE:
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
else:
    AsyncSessionLocal = None

# Sync session maker
SessionLocal = sessionmaker(
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_db() -> AsyncSession:
    """
    Async dependency to provide database session for FastAPI endpoints
    """
    if IS_SQLITE:
        # Fallback to sync for SQLite
        db = SessionLocal()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    else:
        async with AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


def get_sync_db() -> Session:
    """
    Sync dependency to provide database session for FastAPI endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_tables():
    """
    Create all tables defined in the models
    """
    if IS_SQLITE:
        # SQLite: use sync engine
        SQLModel.metadata.create_all(sync_engine)
    else:
        # PostgreSQL: use async engine
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
