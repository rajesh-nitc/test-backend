from fastapi import APIRouter

router: APIRouter = APIRouter()


@router.get("/health")
async def get_health() -> dict[str, str]:
    return {"status": "ok"}
