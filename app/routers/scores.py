from datetime import datetime, timezone
from fastapi import APIRouter, Depends
import aiosqlite

from app.db import get_db
from app.models.scores_model import (
    ScoreCreate,
    ScoreCreated,
    ScoreSummary,
    SubjectSummary,
)

router = APIRouter(prefix="/scores", tags=["Scores"])


@router.post("", response_model=ScoreCreated)
async def create_score(
    payload: ScoreCreate, db: aiosqlite.Connection = Depends(get_db)
):
    created_at = datetime.now(timezone.utc).isoformat()

    cursor = await db.execute(
        """
        INSERT INTO quiz_attempts (created_at, subject, year_group, topic, score, total_questions)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            created_at,
            payload.subject.strip(),
            payload.year_group,
            payload.topic.strip() if payload.topic else None,
            payload.score,
            payload.total_questions,
        ),
    )
    await db.commit()

    return ScoreCreated(id=cursor.lastrowid)


@router.get("/summary", response_model=ScoreSummary)
async def get_summary(db: aiosqlite.Connection = Depends(get_db)):
    overall_row = await (
        await db.execute(
            """
            SELECT
                COUNT(*) AS total_attempts,
                AVG(1.0 * score / total_questions) AS overall_avg_accuracy
            FROM quiz_attempts
            """
        )
    ).fetchone()

    total_attempts = int(overall_row["total_attempts"] or 0)
    overall_avg_accuracy = float(overall_row["overall_avg_accuracy"] or 0.0)

    rows = await (
        await db.execute(
            """
            SELECT
                subject,
                COUNT(*) AS attempts,
                AVG(1.0 * score / total_questions) AS avg_accuracy,
                MAX(1.0 * score / total_questions) AS best_accuracy,
                MIN(1.0 * score / total_questions) AS worst_accuracy
            FROM quiz_attempts
            GROUP BY subject
            ORDER BY avg_accuracy DESC
            """
        )
    ).fetchall()

    by_subject = [
        SubjectSummary(
            subject=r["subject"],
            attempts=int(r["attempts"]),
            avg_accuracy=float(r["avg_accuracy"] or 0.0),
            best_accuracy=float(r["best_accuracy"] or 0.0),
            worst_accuracy=float(r["worst_accuracy"] or 0.0),
        )
        for r in rows
    ]

    return ScoreSummary(
        total_attempts=total_attempts,
        overall_avg_accuracy=overall_avg_accuracy,
        by_subject=by_subject,
    )
