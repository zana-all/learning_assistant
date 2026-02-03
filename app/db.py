import os
import aiosqlite

DB_PATH = os.getenv("LEARNING_ASSISTANT_DB", "app/learning_assistant.db")


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                subject TEXT NOT NULL,
                year_group INTEGER NOT NULL,
                topic TEXT,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL
            )
            """
        )
        await db.commit()


async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()
