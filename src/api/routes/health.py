from fastapi import APIRouter
from ..database.db import ping_database

# Create a router for health endpoints
router = APIRouter(
    prefix="/health",
    tags=["health"],
)

class Health:
    @staticmethod
    @router.get("/")
    async def health_check():
        """
        Health check endpoint to verify the API is running.
        Returns a simple JSON response with status "healthy".
        """
        return {"status db": ping_database()}