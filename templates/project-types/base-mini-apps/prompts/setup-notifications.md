# Setup Notifications with Webhooks

Add notification support to the Base Mini App using webhooks:

## Requirements

1. Create webhook endpoint that:
   - Receives POST requests from Farcaster
   - Validates webhook signatures
   - Processes notification events
   - Returns appropriate responses

2. Implement notification types:
   - User mentions
   - App interactions
   - Custom events
   - System notifications

3. Add webhook configuration:
   - Webhook URL in manifest
   - Signature verification
   - Retry logic for failed deliveries
   - Logging for debugging

4. Create notification handlers:
   - Parse incoming webhook payload
   - Route to appropriate handler
   - Update app state if needed
   - Send acknowledgment

## File Structure

### API Endpoint: api/webhook.ts (or src/api/webhook.ts for Vite)
```typescript
// Implement:
// - POST handler for webhooks
// - Signature verification
// - Event routing
// - Error handling
```

### Types: src/types/notifications.ts
```typescript
// Define types for:
// - Webhook payload
// - Notification events
// - Handler responses
```

### Handlers: src/lib/notifications.ts
```typescript
// Create handlers for:
// - User mentions
// - App interactions
// - Custom events
```

## Manifest Update
Update `public/.well-known/farcaster.json`:
```json
{
  "miniapp": {
    "webhookUrl": "https://your-app.com/api/webhook"
  }
}
```

## Environment Variables
Add to .env:
```
VITE_WEBHOOK_SECRET=your-webhook-secret
VITE_WEBHOOK_URL=https://your-app.com/api/webhook
```

## Testing
1. Create local webhook testing setup
2. Add mock webhook payloads
3. Test signature verification
4. Validate error handling

## Documentation
Update README with:
- Webhook setup instructions
- Event types and payloads
- Testing guidelines
- Troubleshooting tips

Generate all webhook-related code and configuration.
