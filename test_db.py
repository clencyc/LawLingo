import asyncio
from app.database.session import create_tables

async def test_database():
    await create_tables()
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(test_database())