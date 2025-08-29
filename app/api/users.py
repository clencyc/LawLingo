from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.session import get_db
from app.models.user import User

router = APIRouter()

@router.get("/profile")
async def get_profile(user_id: int = 1, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": user.username,
        "email": user.email,
        "avatar": user.avatar,
        "current_country": user.current_country,
        "unlocked_countries": user.unlocked_countries,
        "total_xp": user.total_xp,
        "current_level": user.current_level,
        "current_streak": user.current_streak,
        "learning_preferences": user.learning_preferences,
        "notification_settings": user.notification_settings,
    }

@router.put("/profile")
async def update_profile(user_id: int = 1, db: AsyncSession = Depends(get_db), username: str = None, avatar: str = None):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if username:
        user.username = username
    if avatar:
        user.avatar = avatar
    await db.commit()
    await db.refresh(user)
    return {"message": "Profile updated", "user": user.username}

@router.post("/country/add")
async def add_country(country_code: str, user_id: int = 1, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.unlocked_countries is None:
        user.unlocked_countries = []
    if country_code not in user.unlocked_countries:
        user.unlocked_countries.append(country_code)
    user.current_country = country_code
    await db.commit()
    await db.refresh(user)
    return {"message": f"Country {country_code} set as primary and added to unlocked countries."}