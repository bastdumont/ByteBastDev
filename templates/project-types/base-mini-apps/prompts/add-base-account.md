# Add Base Account Integration

Add Base Account integration to the existing Base Mini App:

## Requirements
1. Create a custom hook `useBaseAccount` that:
   - Retrieves the user's Base Account from Farcaster context
   - Provides account address and connection status
   - Handles errors gracefully

2. Add wallet interaction capabilities:
   - Display user's Base Account address
   - Show account balance
   - Enable transaction signing
   - Support wallet connections

3. Create UI components:
   - AccountDisplay component showing address and balance
   - ConnectButton component
   - TransactionStatus component for pending transactions

4. Implement proper error handling for:
   - No account connected
   - Network errors
   - Transaction failures

5. Add Base Chain configuration:
   - Chain ID: 8453 (Base Mainnet)
   - RPC URL: https://mainnet.base.org
   - Explorer: https://basescan.org

## Code to Generate

### Hook: src/hooks/useBaseAccount.ts
```typescript
// Implement hook that:
// - Gets Base Account from SDK context
// - Fetches account balance
// - Provides transaction signing
// - Handles errors
```

### Component: src/components/AccountDisplay.tsx
```typescript
// Create component that:
// - Shows account address (truncated)
// - Displays balance
// - Has copy address button
// - Shows connection status
```

### Utilities: src/lib/base.ts
```typescript
// Add utilities for:
// - Formatting addresses
// - Formatting balances
// - Building transactions
// - Validating addresses
```

## Integration Steps
1. Update MiniAppWrapper to include Base Account context
2. Add Base Chain config to environment variables
3. Create account-related UI components
4. Add transaction handling logic
5. Include error boundaries
6. Update README with Base Account usage

Generate the necessary code and integration.
