from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.session import get_db
from app.models.user import User

router = APIRouter()

@router.get("/overview")
async def progress_overview(user_id: int = 1, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        return {"current_level": 0, "total_xp": 0, "current_streak": 0, "completed_levels": []}
    return {
        "current_level": user.current_level,
        "total_xp": user.total_xp,
        "current_streak": user.current_streak,
        "completed_levels": [],  # Placeholder for MVP
    }