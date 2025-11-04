from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

from app.core.config import settings


class Database:
    """Database connection manager"""

    client: Optional[AsyncIOMotorClient] = None
    db = None

    async def connect_to_database(self):
        """Connect to MongoDB"""
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.DATABASE_NAME]
        print(f"Connected to MongoDB at {settings.MONGODB_URL}")

    async def close_database_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("Closed MongoDB connection")


database = Database()


async def init_db():
    """Initialize database connection"""
    await database.connect_to_database()


async def close_db():
    """Close database connection"""
    await database.close_database_connection()


def get_database():
    """Get database instance"""
    return database.db
