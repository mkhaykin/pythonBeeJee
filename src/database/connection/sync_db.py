from collections.abc import Generator

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.database.connection.connection import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(engine)  # type: ignore


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
