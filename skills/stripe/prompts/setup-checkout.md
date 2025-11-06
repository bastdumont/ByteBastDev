# Setup Stripe Checkout

Implement Stripe Checkout for quick payment collection:

## Checkout Configuration
- **Mode**: {mode} (payment, subscription, setup)
- **Products**: {products_list}
- **Success URL**: {success_url}
- **Cancel URL**: {cancel_url}

## Requirements

### 1. Checkout Session Creation

**Backend Endpoint** (`/api/create-checkout-session`)
```typescript
// Create checkout session
POST /api/create-checkout-session
{
  "mode": "payment" | "subscription" | "setup",
  "line_items": [
    {
      "price": "price_123",
      "quantity": 1
    }
  ],
  "success_url": "https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
  "cancel_url": "https://example.com/cancel",
  "customer_email": "customer@example.com" // optional
}
```

**Implementation**
- Validate request parameters
- Create Stripe Checkout session
- Return session ID and URL
- Handle errors appropriately
- Add metadata for tracking

### 2. Frontend Integration

**Redirect to Checkout**
```typescript
// React example
const handleCheckout = async () => {
  const response = await fetch('/api/create-checkout-session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      mode: 'payment',
      line_items: selectedItems
    })
  });

  const { url } = await response.json();
  window.location.href = url;
};
```

**Buy Button Component**
```typescript
<CheckoutButton
  items={items}
  mode="payment"
  onSuccess={handleSuccess}
  onError={handleError}
/>
```

### 3. Success & Cancel Pages

**Success Page** (`/success`)
- Retrieve session with session_id query param
- Display order confirmation
- Show order details
- Provide next steps
- Send confirmation email

```typescript
// Verify session
const session = await stripe.checkout.sessions.retrieve(sessionId);
if (session.payment_status === 'paid') {
  // Order fulfilled
}
```

**Cancel Page** (`/cancel`)
- Display cancellation message
- Offer to retry
- Provide support contact
- Log cancellation

### 4. Webhook Integration

Handle Checkout events:
```typescript
// Webhook handler
switch (event.type) {
  case 'checkout.session.completed':
    const session = event.data.object;
    // Fulfill order
    await fulfillOrder(session);
    break;

  case 'checkout.session.async_payment_succeeded':
    // Handle async payment success
    break;

  case 'checkout.session.async_payment_failed':
    // Handle async payment failure
    break;
}
```

### 5. Product Configuration

**For Payment Mode**
- Set up products and prices in Stripe
- Support one-time payments
- Handle quantity selection
- Apply coupons/discounts

**For Subscription Mode**
- Configure recurring prices
- Set trial periods
- Handle plan selection
- Apply promotional codes

**For Setup Mode**
- Save payment method for future use
- No immediate charge
- Useful for account setup

### 6. Customization Options

**Session Options**
```typescript
const session = await stripe.checkout.sessions.create({
  mode: 'payment',
  line_items: [...],
  success_url: '...',
  cancel_url: '...',

  // Optional customizations
  allow_promotion_codes: true,
  billing_address_collection: 'required',
  shipping_address_collection: {
    allowed_countries: ['US', 'CA', 'GB']
  },
  phone_number_collection: {
    enabled: true
  },
  custom_text: {
    submit: {
      message: 'Complete your purchase'
    }
  },
  metadata: {
    order_id: 'order_123',
    user_id: 'user_456'
  }
});
```

### 7. Mobile Optimization
- Responsive design
- Mobile payment methods (Apple Pay, Google Pay)
- Touch-friendly buttons
- Fast loading times
- Progressive enhancement

## File Structure
```
src/
  ├── components/
  │   ├── CheckoutButton.tsx
  │   ├── ProductCard.tsx
  │   └── SuccessMessage.tsx
  ├── pages/
  │   ├── checkout.tsx
  │   ├── success.tsx
  │   └── cancel.tsx
  ├── api/
  │   ├── create-checkout-session.ts
  │   └── webhooks/
  │       └── stripe.ts
  └── lib/
      └── stripe.ts
```

## Features to Implement

### Product Display
- Show product images
- Display pricing
- List features/description
- Quantity selector
- Add to cart (if multi-product)
- Display total

### Checkout Flow
1. User clicks checkout button
2. Create checkout session
3. Redirect to Stripe Checkout
4. User completes payment
5. Redirect to success page
6. Fulfill order via webhook

### Post-Checkout
- Order confirmation page
- Email receipt
- Update inventory
- Create customer account
- Grant access to digital products

## Payment Methods
Support multiple payment methods:
- Cards (Visa, Mastercard, Amex)
- Digital wallets (Apple Pay, Google Pay)
- Bank transfers (ACH, SEPA)
- Buy now, pay later (Klarna, Afterpay)
- Local payment methods

Enable in Checkout session:
```typescript
payment_method_types: [
  'card',
  'apple_pay',
  'google_pay',
  'klarna',
  'afterpay_clearpay'
]
```

## Discount & Promotion Codes

**Allow Promotion Codes**
```typescript
const session = await stripe.checkout.sessions.create({
  allow_promotion_codes: true,
  // ...
});
```

**Apply Coupon Directly**
```typescript
const session = await stripe.checkout.sessions.create({
  discounts: [{
    coupon: 'SUMMER20'
  }],
  // ...
});
```

## Shipping & Tax

**Collect Shipping Address**
```typescript
shipping_address_collection: {
  allowed_countries: ['US', 'CA', 'GB', 'FR', 'DE']
}
```

**Calculate Shipping**
```typescript
shipping_options: [
  {
    shipping_rate_data: {
      type: 'fixed_amount',
      fixed_amount: {
        amount: 500,
        currency: 'usd'
      },
      display_name: 'Standard shipping',
      delivery_estimate: {
        minimum: { unit: 'business_day', value: 5 },
        maximum: { unit: 'business_day', value: 7 }
      }
    }
  }
]
```

**Tax Calculation**
- Enable automatic tax in Stripe Dashboard
- Or use Stripe Tax API
- Display tax in checkout

## Testing
Test scenarios:
- [ ] Successful payment
- [ ] Declined payment
- [ ] User cancels checkout
- [ ] Expired session (24 hours)
- [ ] Multiple items
- [ ] Promotion code applied
- [ ] Different payment methods
- [ ] Mobile checkout
- [ ] Webhook received
- [ ] Order fulfilled

## Analytics
Track checkout metrics:
- Checkout initiated
- Checkout completed
- Abandonment rate
- Conversion rate
- Average order value
- Revenue by product
- Payment method usage

## Error Handling
Handle errors gracefully:
- Session creation failed
- Payment declined
- Network errors
- Session expired
- Invalid products/prices
- Server errors

## Security
- Validate session on success page
- Verify webhook signatures
- Use HTTPS
- Don't trust client-side session data
- Check payment status before fulfillment
- Implement idempotency

Generate all necessary code and configuration.
