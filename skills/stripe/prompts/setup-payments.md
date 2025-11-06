# Setup Stripe Payments

Implement a complete Stripe payment system with the following specifications:

## Payment Configuration
- **Payment Type**: {payment_type} (one-time, subscription, both)
- **Currency**: {currency}
- **Supported Methods**: {payment_methods} (card, bank transfer, etc.)

## Requirements

### 1. Backend Setup
Create the following API endpoints:

**Payment Intent Endpoint** (`/api/create-payment-intent`)
- Accept amount, currency, and metadata
- Create Stripe Payment Intent
- Return client secret for frontend
- Include idempotency key handling
- Implement error handling

**Webhook Endpoint** (`/api/webhooks/stripe`)
- Verify webhook signature
- Handle payment lifecycle events:
  - `payment_intent.succeeded`
  - `payment_intent.payment_failed`
  - `payment_intent.canceled`
- Update order/transaction status
- Send confirmation emails
- Log all events

### 2. Frontend Integration
Create payment collection components:

**Checkout Component**
- Integrate Stripe Elements
- Collect card information securely
- Display payment errors
- Show loading states
- Handle successful payment
- Support billing details collection

**Payment Form**
- Card number element
- Expiry date element
- CVC element
- Postal code (if required)
- Custom styling to match brand
- Real-time validation
- Error messages

### 3. Configuration Files

**Environment Variables** (`.env`)
```
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

**Stripe Config** (`stripe-config.ts`)
- Initialize Stripe with publishable key
- Configure Elements appearance
- Set locale and currency

### 4. Error Handling
Handle the following error scenarios:
- Card declined
- Insufficient funds
- Expired card
- Incorrect CVC
- Network errors
- Server errors
- Rate limiting

### 5. Security Measures
- Never send card data to server
- Use Stripe.js/Elements for card collection
- Verify webhook signatures
- Use HTTPS only
- Implement CSRF protection
- Rate limit API endpoints

### 6. Testing Setup
Include test configuration:
- Use test API keys
- Test card numbers
- Webhook testing with Stripe CLI
- Success and failure scenarios

## File Structure
```
src/
  ├── components/
  │   ├── CheckoutForm.tsx
  │   ├── PaymentStatus.tsx
  │   └── StripeWrapper.tsx
  ├── lib/
  │   ├── stripe.ts
  │   └── stripe-config.ts
  └── api/
      ├── create-payment-intent.ts
      └── webhooks/
          └── stripe.ts
```

## Implementation Notes
- Use TypeScript for type safety
- Implement proper loading states
- Add user feedback for all actions
- Log important events
- Handle edge cases
- Support mobile browsers
- Add analytics tracking

## Testing Checklist
- [ ] Successful payment with test card (4242 4242 4242 4242)
- [ ] Declined payment with decline card (4000 0000 0000 0002)
- [ ] 3D Secure authentication (4000 0027 6000 3184)
- [ ] Webhook events received and processed
- [ ] Error messages display correctly
- [ ] Loading states work properly
- [ ] Mobile responsive

Generate all necessary code, configuration, and documentation.
