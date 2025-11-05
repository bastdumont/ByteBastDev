from pydantic import BaseModel, Field, field_validator
from pydantic_core import core_schema
from typing import List, Optional, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(str):
    """Custom ObjectId type for Pydantic v2"""
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler):
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ])
        ],
        serialization=core_schema.plain_serializer_function_ser_schema(
            lambda x: str(x) if isinstance(x, ObjectId) else x
        ))

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            return v
        raise ValueError("Invalid ObjectId")

class StockHolding(BaseModel):
    """Individual stock holding"""
    symbol: str
    quantity: float
    purchase_price: float
    purchase_date: datetime
    current_price: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "quantity": 10.0,
                "purchase_price": 150.00,
                "purchase_date": "2024-01-01T00:00:00"
            }
        }

class Portfolio(BaseModel):
    """Portfolio model"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None, serialization_alias="id")
    user_id: str
    name: str
    description: Optional[str] = None
    holdings: List[StockHolding] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "user_id": "user123",
                "name": "Tech Growth Portfolio",
                "description": "Focus on technology stocks",
                "holdings": []
            }
        }
    }

class PortfolioCreate(BaseModel):
    """Portfolio creation model"""
    name: str
    description: Optional[str] = None

class PortfolioUpdate(BaseModel):
    """Portfolio update model"""
    name: Optional[str] = None
    description: Optional[str] = None
