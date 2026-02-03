from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["Default"])


@router.get("/health")
def health():
    return {"status": "ok"}
