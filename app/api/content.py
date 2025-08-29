from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.session import get_db
from app.models.country import Country

router = APIRouter()

@router.get("/countries")
async def list_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country))
    countries = result.scalars().all()
    return [{"code": c.code, "name": c.name, "flag_url": c.flag_url} for c in countries]

@router.get("/countries/{country_code}/constitution")
async def get_constitution(country_code: str):
    # Placeholder for MVP
    return {"country_code": country_code, "constitution": "Constitution text here"}