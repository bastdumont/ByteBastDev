from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel

app = FastAPI(
    title="{{project_name}} API",
    version="1.0.0",
    description="FastAPI backend for full-stack monorepo"
)

# CORS configuration for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    message: str
    timestamp: str
    status: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to {{project_name}} API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        message="API is running",
        timestamp=datetime.utcnow().isoformat(),
        status="healthy"
    )


@app.get("/api/v1/items")
async def get_items():
    """Get all items"""
    return {
        "items": [
            {"id": 1, "name": "Item 1", "price": 10.99},
            {"id": 2, "name": "Item 2", "price": 20.99},
            {"id": 3, "name": "Item 3", "price": 30.99},
        ]
    }


@app.post("/api/v1/items")
async def create_item(item: Item):
    """Create a new item"""
    return {
        "success": True,
        "item": item.dict(),
        "message": "Item created successfully"
    }


@app.get("/api/v1/items/{item_id}")
async def get_item(item_id: int):
    """Get item by ID"""
    return {
        "id": item_id,
        "name": f"Item {item_id}",
        "price": 10.99 * item_id
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
