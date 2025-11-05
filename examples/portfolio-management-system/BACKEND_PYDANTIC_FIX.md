# Backend Pydantic v2 Compatibility Fix

## Issue

When trying to create a portfolio from the frontend, users encountered:
```
Error creating portfolio: Network Error
```

## Root Cause

The backend was using **Pydantic v1 style** validators for the `PyObjectId` class, but the actual Pydantic version installed was **v2**. This caused two main issues:

1. **Validation Error**: `TypeError: PyObjectId.validate() takes 2 positional arguments but 3 were given`
2. **Serialization Error**: `PydanticSerializationError: Unable to serialize unknown type: <class 'bson.objectid.ObjectId'>`
3. **Field Naming**: API was returning `_id` but frontend expected `id`

## Solution

Updated [backend/app/models/portfolio.py](backend/app/models/portfolio.py) to use Pydantic v2 syntax:

### 1. Updated PyObjectId Class

**Before (Pydantic v1 style):**
```python
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
```

**After (Pydantic v2 style):**
```python
from pydantic_core import core_schema

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
```

### 2. Updated Portfolio Model Config

**Before:**
```python
class Config:
    populate_by_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}
```

**After:**
```python
model_config = {
    "populate_by_name": True,
    "arbitrary_types_allowed": True,
    "json_encoders": {ObjectId: str},
}
```

### 3. Fixed Field Serialization

**Before:**
```python
id: Optional[PyObjectId] = Field(alias="_id", default=None)
```

**After:**
```python
id: Optional[PyObjectId] = Field(alias="_id", default=None, serialization_alias="id")
```

This ensures:
- Database reads using `_id` (MongoDB convention)
- API responses use `id` (frontend expectation)

## Changes Made

### Files Modified
- [backend/app/models/portfolio.py](backend/app/models/portfolio.py)

### Imports Added
```python
from pydantic import BaseModel, Field, field_validator
from pydantic_core import core_schema
from typing import List, Optional, Any
```

## Testing

### Before Fix
```bash
curl http://localhost:8000/api/v1/portfolios
# Result: Internal Server Error
```

### After Fix
```bash
curl http://localhost:8000/api/v1/portfolios
# Result: [{"id":"690b5500e6bdeba239422585","user_id":"demo_user",...}]

curl -X POST http://localhost:8000/api/v1/portfolios \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "description": "Testing"}'
# Result: {"id":"690b58d2ecbc1a436075c96e","user_id":"demo_user",...}
```

## Impact

- ✅ Fixed portfolio creation from frontend
- ✅ Fixed portfolio listing
- ✅ Fixed all CRUD operations
- ✅ API now returns `id` field (not `_id`)
- ✅ Proper ObjectId serialization to string
- ✅ Compatible with Pydantic v2

## Pydantic v1 vs v2 Differences

| Feature | Pydantic v1 | Pydantic v2 |
|---------|-------------|-------------|
| Config | `class Config:` | `model_config = {}` |
| Validators | `__get_validators__` | `__get_pydantic_core_schema__` |
| Serialization | `json_encoders` dict | `core_schema` serialization |
| Type Hints | More lenient | Stricter typing |

## Additional Notes

### Why Inherit from `str` Instead of `ObjectId`?

In Pydantic v2, custom types that inherit from built-in types (like `str`) are easier to serialize. By making `PyObjectId` inherit from `str`:
- Automatic string serialization
- Compatible with JSON responses
- Proper validation still occurs via custom schema

### Serialization Schema

The `plain_serializer_function_ser_schema` ensures that:
1. `ObjectId` instances are converted to strings
2. String values pass through unchanged
3. Serialization happens automatically in API responses

## Frontend Compatibility

The frontend expects this structure:
```typescript
interface Portfolio {
  id: string;  // Not _id
  user_id: string;
  name: string;
  description?: string;
  holdings: StockHolding[];
  created_at: string;
  updated_at: string;
}
```

With `serialization_alias="id"`, the API now correctly returns:
```json
{
  "id": "690b5500e6bdeba239422585",
  "user_id": "demo_user",
  "name": "Portfolio Name",
  ...
}
```

## How to Apply This Fix

If you encounter similar issues in other projects:

1. **Update imports:**
   ```python
   from pydantic_core import core_schema
   ```

2. **Update custom types:**
   - Replace `__get_validators__` with `__get_pydantic_core_schema__`
   - Add serialization schema
   - Inherit from built-in types when possible

3. **Update model config:**
   - Replace `class Config:` with `model_config = {}`

4. **Add serialization aliases:**
   - Use `serialization_alias` for different input/output field names

## Verification

To verify the fix is working:

```bash
# Test list portfolios
curl http://localhost:8000/api/v1/portfolios

# Test create portfolio
curl -X POST http://localhost:8000/api/v1/portfolios \
  -H "Content-Type: application/json" \
  -d '{"name": "New Portfolio", "description": "Test"}'

# Check frontend can create portfolios
# Open http://localhost:3000 and create a portfolio
```

## Status

✅ **Fixed and Tested**

The backend now works correctly with:
- Pydantic v2
- Frontend API calls
- Portfolio CRUD operations
- ObjectId serialization

---

**Fix Applied**: November 2025
**Issue**: Pydantic v1/v2 compatibility
**Status**: ✅ Resolved
