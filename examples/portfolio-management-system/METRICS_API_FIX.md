# Portfolio Metrics API Field Mismatch Fix

## Issue

When clicking on a portfolio to view details, the frontend displayed this error:

```
ERROR
Cannot read properties of undefined (reading 'toLocaleString')
TypeError: Cannot read properties of undefined (reading 'toLocaleString')
    at PortfolioMetrics (http://localhost:3000/static/js/bundle.js:98681:47)
```

## Root Cause

**Frontend-Backend Field Name Mismatch**

The backend API was returning different field names than what the frontend expected:

| Backend Returns | Frontend Expected |
|----------------|-------------------|
| `current_value` | `total_value` |
| `total_invested` | `total_cost` |
| `gain_loss` | `total_gain_loss` |
| `gain_loss_percentage` | `total_gain_loss_percent` |
| `num_holdings` | `holdings_count` |

### Backend Response (Actual)
```json
{
  "current_value": 0,
  "total_invested": 0,
  "gain_loss": 0,
  "gain_loss_percentage": 0,
  "num_holdings": 0
}
```

### Frontend Expected
```typescript
interface PortfolioMetrics {
  total_value: number;
  total_cost: number;
  total_gain_loss: number;
  total_gain_loss_percent: number;
  holdings_count: number;
}
```

## Solution

Updated the frontend to match the backend API response format.

### Files Modified

1. **[frontend/src/types/index.ts](frontend/src/types/index.ts)**
   - Updated `PortfolioMetrics` interface to match backend field names

2. **[frontend/src/components/PortfolioMetrics.tsx](frontend/src/components/PortfolioMetrics.tsx)**
   - Updated component to use correct field names from API response
   - Added safe extraction with nullish coalescing (`??`)

## Changes Made

### 1. Updated TypeScript Types

**Before:**
```typescript
export interface PortfolioMetrics {
  total_value: number;
  total_cost: number;
  total_gain_loss: number;
  total_gain_loss_percent: number;
  holdings_count: number;
}
```

**After:**
```typescript
export interface PortfolioMetrics {
  // Backend returns these field names
  current_value: number;
  total_invested: number;
  gain_loss: number;
  gain_loss_percentage: number;
  num_holdings: number;
}
```

### 2. Updated Component Logic

**Before:**
```typescript
const isPositive = metrics.total_gain_loss >= 0;

${metrics.total_value.toLocaleString(...)}
${metrics.total_cost.toLocaleString(...)}
${metrics.total_gain_loss.toLocaleString(...)}
{metrics.total_gain_loss_percent.toFixed(2)}%
{metrics.holdings_count}
```

**After:**
```typescript
// Extract values from metrics (backend uses these field names)
const totalValue = metrics.current_value ?? 0;
const totalCost = metrics.total_invested ?? 0;
const gainLoss = metrics.gain_loss ?? 0;
const gainLossPercent = metrics.gain_loss_percentage ?? 0;
const holdingsCount = metrics.num_holdings ?? 0;

const isPositive = gainLoss >= 0;

${totalValue.toLocaleString(...)}
${totalCost.toLocaleString(...)}
${gainLoss.toLocaleString(...)}
{gainLossPercent.toFixed(2)}%
{holdingsCount}
```

## Benefits of This Approach

1. **Type Safety**: TypeScript types now match actual API response
2. **Null Safety**: Using nullish coalescing (`??`) prevents undefined errors
3. **Clarity**: Variable names clearly show data source
4. **Maintainability**: Easy to understand field mapping

## Testing

### Before Fix
```
✗ Click portfolio → Runtime error
✗ Portfolio metrics not displayed
✗ Page crashes with undefined error
```

### After Fix
```bash
# Test the API
curl http://localhost:8000/api/v1/portfolios/{id}/metrics

# Response:
{
  "current_value": 0,
  "total_invested": 0,
  "gain_loss": 0,
  "gain_loss_percentage": 0,
  "num_holdings": 0
}
```

```
✓ Click portfolio → Loads successfully
✓ Portfolio metrics displayed correctly
✓ All values show as $0.00 (for empty portfolio)
✓ No runtime errors
```

## Why This Happened

The backend was implemented with one set of field names (matching typical financial terminology), while the frontend was built expecting different names. This is a common issue when:

1. Backend and frontend developed separately
2. API contract not clearly defined
3. Different naming conventions used

## Prevention

To prevent similar issues in the future:

1. **API Contract First**: Define API response structure before implementation
2. **Shared Types**: Consider generating TypeScript types from backend models
3. **Integration Testing**: Test frontend-backend integration early
4. **Documentation**: Keep API documentation up to date

## Alternative Solutions

### Option 1: Change Backend (Not Recommended)
Could update backend to use frontend's expected field names, but:
- Requires backend code changes
- May break other integrations
- More disruptive

### Option 2: API Translation Layer (Overkill)
Could create middleware to transform responses, but:
- Adds complexity
- Unnecessary for simple field mapping
- Performance overhead

### Option 3: Update Frontend (Chosen) ✅
Update frontend types and component:
- Minimal changes
- Type-safe
- Clear mapping
- No backend changes needed

## Related Files

- Backend metrics calculation: [backend/app/services/portfolio_service.py](backend/app/services/portfolio_service.py#L162)
- Backend metrics endpoint: [backend/app/api/portfolios.py](backend/app/api/portfolios.py#L127)
- Frontend types: [frontend/src/types/index.ts](frontend/src/types/index.ts)
- Frontend component: [frontend/src/components/PortfolioMetrics.tsx](frontend/src/components/PortfolioMetrics.tsx)

## Status

✅ **Fixed and Deployed**

The portfolio detail page now works correctly and displays:
- Total Value
- Total Cost (Investment)
- Gain/Loss ($ and %)
- Number of Holdings

All values display as $0.00 for empty portfolios, and will update when holdings are added.

---

**Fix Applied**: November 2025
**Issue**: Frontend-Backend field name mismatch
**Status**: ✅ Resolved
