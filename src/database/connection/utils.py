from collections.abc import Callable
from functools import wraps
from logging import getLogger
from typing import Any, ParamSpec, TypeVar

from flask import abort
from sqlalchemy import select, text
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection.async_db import async_engine
from src.database.connection.sync_db import engine
from src.database.model.base import Base

logger = getLogger(__name__)
P = ParamSpec("P")
R = TypeVar("R")


async def ping_db(session: AsyncSession) -> bool:
    try:
        await session.execute(select(text("1")))
    except:  # noqa
        return False
    return True


async def async_create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def async_drop_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    Base.metadata.drop_all(bind=engine)


def db_error_wrapper(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
        session: AsyncSession = kwargs.get("session", NotImplemented)  # type: ignore
        try:
            result = await func(*args, **kwargs)
        except IntegrityError as err:
            await session.rollback()
            logger.debug(f"IntegrityError. Message: {err}")
            raise abort(409, "Ошибка создания/изменения данных.")
        except DatabaseError as err:
            await session.rollback()
            logger.debug(f"DatabaseError. Message: {err}")
            raise abort(424, "Ошибка работы с БД.")
        except OSError as err:
            logger.debug(f"OSError. Message: {err}")
            raise abort(500, "Ошибка работы с БД.")

        return result

    return wrapper
