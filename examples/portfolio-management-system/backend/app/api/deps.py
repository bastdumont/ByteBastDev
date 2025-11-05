from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings

# Database client (singleton)
_db_client: AsyncIOMotorClient = None

async def get_db() -> AsyncIOMotorDatabase:
    """Get database instance"""
    global _db_client

    if _db_client is None:
        _db_client = AsyncIOMotorClient(settings.MONGODB_URL)

    return _db_client[settings.DATABASE_NAME]

async def get_current_user_stub():
    """
    Stub for authentication - returns default user
    In production, implement proper JWT authentication
    """
    return "demo_user"
