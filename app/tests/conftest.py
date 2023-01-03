from typing import Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db import get_session
from app.main import app
from app.models.base import Base
from app.settings import Settings

settings = Settings()


@pytest.fixture
async def ac() -> Generator:
    async with AsyncClient(app=app, base_url="https://test") as c:
        yield c


@pytest.fixture(scope="session")
def setup_db() -> Generator:
    engine = create_engine(f"{settings.DB_URI.replace('+asyncpg', '')}")
    conn = engine.connect()
    # トランザクションを一度終了させる
    conn.execute("commit")
    try:
        conn.execute("drop database test")
    except SQLAlchemyError:
        pass
    finally:
        conn.close()

    conn = engine.connect()
    # トランザクションを一度終了させる
    conn.execute("commit")
    conn.execute("create database test")
    conn.close()

    yield

    conn = engine.connect()
    # トランザクションを一度終了させる
    conn.execute("commit")
    try:
        conn.execute("drop database test")
    except SQLAlchemyError:
        pass
    conn.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db(setup_db):
    engine = create_engine(f"{settings.DB_URI.replace('+asyncpg', '')}/test")

    with engine.begin():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        yield
        Base.metadata.drop_all(engine)


@pytest.fixture
async def session():
    # https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    async_engine = create_async_engine(f"{settings.DB_URI}/test")
    async with async_engine.connect() as conn:

        await conn.begin()
        await conn.begin_nested()
        AsyncSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
            future=True,
            class_=AsyncSession,
        )

        async_session = AsyncSessionLocal()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction:
                conn.sync_connection.begin_nested()

        def test_get_session() -> Generator:
            try:
                yield AsyncSessionLocal
            except SQLAlchemyError:
                pass

        app.dependency_overrides[get_session] = test_get_session

        yield async_session
        await async_session.close()
        await conn.rollback()
