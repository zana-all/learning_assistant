from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import lesson, quiz, default, scores
from app.db import init_db
from contextlib import asynccontextmanager


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup logic
        await init_db()
        yield

    app = FastAPI(lifespan=lifespan, title="Learning Assistant API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(default.router)
    app.include_router(lesson.router)
    app.include_router(quiz.router)
    app.include_router(scores.router)
    return app


app = create_app()
