from fastapi import APIRouter, Depends, Query

from auth import get_current_user
from database import get_user_video_history

router = APIRouter(prefix="/api", tags=["history"])


@router.get("/history")
async def get_history(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user: dict = Depends(get_current_user),
):
    items, total = get_user_video_history(user["id"], offset=offset, limit=limit)
    return {
        "success": True,
        "data": {
            "items": items,
            "total": total,
            "has_more": offset + len(items) < total,
        },
    }
