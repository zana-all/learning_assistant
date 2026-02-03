import os
import tempfile

import aiosqlite
import pytest
import pytest_asyncio
from fastapi import FastAPI

from app.db import get_db
from app.routers.scores import router as scores_router


@pytest_asyncio.fixture
async def db_conn():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    conn = await aiosqlite.connect(path)
    conn.row_factory = aiosqlite.Row

    # Create schema needed for scores endpoints
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            subject TEXT NOT NULL,
            year_group INTEGER NOT NULL,
            topic TEXT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL
        )
        """
    )
    await conn.commit()

    try:
        yield conn
    finally:
        await conn.close()
        try:
            os.remove(path)
        except OSError:
            pass


@pytest.fixture
def app(db_conn):
    test_app = FastAPI()
    test_app.include_router(scores_router)

    async def override_get_db():
        yield db_conn

    test_app.dependency_overrides[get_db] = override_get_db
    return test_app
