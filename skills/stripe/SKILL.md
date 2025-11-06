# Stripe Payment Processing Skill

## Overview
This skill provides comprehensive integration with Stripe's payment processing platform. It enables developers to quickly implement payment flows, subscription management, customer handling, and financial operations in their applications.

## Capabilities
- Accept online payments with Payment Intents
- Create and manage subscriptions
- Handle customer data and payment methods
- Generate invoices and process refunds
- Create products, prices, and coupons
- Set up Stripe Checkout sessions
- Handle webhooks for real-time events
- Manage disputes and fraud prevention
- Track balance and payouts
- Generate integration code for popular frameworks

## Prerequisites
- Stripe account (sign up at [stripe.com](https://stripe.com))
- API keys (test and live)
- Webhook endpoint (for production)

## Technologies
- **Platform**: Stripe API v1
- **SDKs**: stripe-node, stripe-python, stripe-php, etc.
- **Frontend**: Stripe.js, React Stripe.js, Stripe Elements
- **Webhooks**: Event-driven architecture
- **Security**: PCI-DSS compliant

## Core Concepts

### API Keys
Stripe uses API keys to authenticate requests:
- **Publishable Key**: Used in client-side code (safe to expose)
- **Secret Key**: Used in server-side code (keep confidential)
- **Test vs Live**: Use test keys for development, live keys for production

```bash
# Test keys
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Payment Flow
1. **Client**: Collect payment details securely with Stripe.js
2. **Server**: Create Payment Intent with amount and currency
3. **Client**: Confirm payment with collected payment method
4. **Server**: Handle webhook events for payment lifecycle

### Subscription Flow
1. Create Product and Price
2. Create Customer
3. Attach Payment Method to Customer
4. Create Subscription with Price ID
5. Handle subscription lifecycle events via webhooks

## Payment Operations

### Create Payment Intent

```python
# Python example
payment_intent = await stripe_adapter.create_payment_intent(
    amount=2000,  # $20.00 in cents
    currency='usd',
    customer_id='cus_123',
    metadata={
        'order_id': 'order_123',
        'user_id': 'user_456'
    }
)
```

### Create Checkout Session

```python
# Create a hosted checkout page
session = await stripe_adapter.create_checkout_session(
    line_items=[
        {
            'price': 'price_123',
            'quantity': 1
        }
    ],
    mode='payment',
    success_url='https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='https://example.com/cancel',
    customer_email='customer@example.com'
)

# Redirect user to session.url
```

### Process Refund

```python
# Full refund
refund = await stripe_adapter.create_refund(
    payment_intent_id='pi_123',
    reason='requested_by_customer'
)

# Partial refund
refund = await stripe_adapter.create_refund(
    payment_intent_id='pi_123',
    amount=1000,  # Refund $10.00
    reason='requested_by_customer'
)
```

## Customer Management

### Create Customer

```python
customer = await stripe_adapter.create_customer(
    email='customer@example.com',
    name='John Doe',
    metadata={
        'user_id': 'user_123'
    }
)
```

### Attach Payment Method

```python
# Attach a payment method to customer
result = await stripe_adapter.attach_payment_method(
    payment_method_id='pm_123',
    customer_id='cus_123'
)
```

### List Customers

```python
customers = await stripe_adapter.list_customers(
    limit=100,
    email='specific@example.com'  # Optional filter
)
```

## Subscription Management

### Create Product and Price

```python
# Create product
product = await stripe_adapter.create_product(
    name='Premium Subscription',
    description='Access to all premium features',
    images=['https://example.com/product.jpg']
)

# Create monthly price
price = await stripe_adapter.create_price(
    product_id=product['product_id'],
    unit_amount=2999,  # $29.99
    currency='usd',
    recurring={
        'interval': 'month',
        'interval_count': 1
    }
)
```

### Create Subscription

```python
subscription = await stripe_adapter.create_subscription(
    customer_id='cus_123',
    items=[
        {
            'price': 'price_123',
            'quantity': 1
        }
    ],
    trial_period_days=14,  # Optional trial
    metadata={
        'plan': 'premium'
    }
)
```

### Update Subscription

```python
# Upgrade/downgrade subscription
updated_sub = await stripe_adapter.update_subscription(
    subscription_id='sub_123',
    updates={
        'items': [
            {
                'id': 'si_123',  # Existing item
                'price': 'price_456'  # New price
            }
        ],
        'proration_behavior': 'create_prorations'
    }
)
```

### Cancel Subscription

```python
# Cancel at end of billing period
canceled_sub = await stripe_adapter.cancel_subscription(
    subscription_id='sub_123',
    immediately=False
)

# Cancel immediately
canceled_sub = await stripe_adapter.cancel_subscription(
    subscription_id='sub_123',
    immediately=True
)
```

## Invoice Management

### Create and Send Invoice

```python
# Create invoice
invoice = await stripe_adapter.create_invoice(
    customer_id='cus_123',
    collection_method='send_invoice',
    days_until_due=30
)

# Finalize invoice (makes it payable)
finalized = await stripe_adapter.finalize_invoice(
    invoice_id=invoice['invoice_id']
)
```

## Coupons and Promotions

### Create Coupon

```python
# Percentage discount
coupon = await stripe_adapter.create_coupon(
    duration='forever',
    percent_off=20,
    name='20% Off'
)

# Fixed amount discount
coupon = await stripe_adapter.create_coupon(
    duration='once',
    amount_off=500,  # $5.00
    currency='usd',
    name='$5 Off First Purchase'
)

# Repeating discount
coupon = await stripe_adapter.create_coupon(
    duration='repeating',
    percent_off=10,
    duration_in_months=3,
    name='10% Off for 3 Months'
)
```

### Create Promotion Code

```python
promo = await stripe_adapter.create_promotion_code(
    coupon_id='coup_123',
    code='SAVE20',
    max_redemptions=100
)
```

## Webhook Handling

### Setup Webhook Endpoint

```python
webhook = await stripe_adapter.create_webhook_endpoint(
    url='https://example.com/api/webhooks/stripe',
    enabled_events=[
        'payment_intent.succeeded',
        'payment_intent.payment_failed',
        'customer.subscription.created',
        'customer.subscription.updated',
        'customer.subscription.deleted',
        'invoice.paid',
        'invoice.payment_failed'
    ],
    description='Main webhook endpoint'
)

# Save webhook secret for signature verification
webhook_secret = webhook['secret']
```

### Verify and Process Webhook

```python
# In your webhook handler
event = await stripe_adapter.construct_webhook_event(
    payload=request.body,
    signature=request.headers['stripe-signature'],
    webhook_secret='whsec_...'
)

if event['verified']:
    event_type = event['event_type']

    if event_type == 'payment_intent.succeeded':
        # Handle successful payment
        pass
    elif event_type == 'customer.subscription.updated':
        # Handle subscription update
        pass
```

## Common Integration Patterns

### Payment Link (No-Code)

```python
# Create shareable payment link
link = await stripe_adapter.create_payment_link(
    line_items=[
        {
            'price': 'price_123',
            'quantity': 1
        }
    ],
    after_completion_url='https://example.com/thank-you'
)

# Share link['url'] with customers
```

### Subscription Billing Portal

Stripe provides a hosted customer portal for subscription management:
- Update payment methods
- Cancel subscriptions
- View billing history
- Download invoices

```python
# Generate portal session
# (Done via Stripe Dashboard or API)
portal_url = "https://billing.stripe.com/session/..."
```

### Save Card for Future Payments

```python
# Use Setup Intent to save payment method
setup_intent = await stripe_adapter.create_payment_intent(
    amount=0,  # No charge
    currency='usd',
    customer_id='cus_123',
    setup_future_usage='off_session'
)

# After confirmation, payment method is saved to customer
```

## Code Generation

### Generate Checkout Integration

```python
# Generate React Stripe Checkout integration
result = await stripe_adapter.generate_checkout_integration(
    framework='react',
    mode='payment',
    output_dir='./src/components'
)

# Creates:
# - checkout.tsx
# - stripe-config.ts
# - api/create-checkout-session.ts
```

### Generate Subscription Integration

```python
# Generate subscription management UI
result = await stripe_adapter.generate_subscription_integration(
    framework='react',
    output_dir='./src/features/subscription'
)

# Creates:
# - subscription-manager.tsx
# - pricing-table.tsx
# - api/subscription.ts
# - hooks/useSubscription.ts
```

### Generate Webhook Handler

```python
# Generate webhook handler
result = await stripe_adapter.generate_webhook_handler(
    platform='node',
    events=[
        'payment_intent.succeeded',
        'customer.subscription.updated'
    ],
    output_dir='./api/webhooks'
)

# Creates:
# - webhook-handler.ts
# - event-handlers.ts
```

## Best Practices

### Security
- **Never expose secret keys**: Keep secret keys server-side only
- **Verify webhooks**: Always verify webhook signatures
- **Use HTTPS**: All API calls and webhooks must use HTTPS
- **Idempotency**: Use idempotency keys for payment operations
- **Handle errors**: Implement proper error handling and retries

### Testing
- **Test mode**: Use test API keys during development
- **Test cards**: Use Stripe's test card numbers
  - Success: 4242 4242 4242 4242
  - Decline: 4000 0000 0000 0002
  - 3D Secure: 4000 0027 6000 3184
- **Webhook testing**: Use Stripe CLI for local webhook testing

```bash
stripe listen --forward-to localhost:3000/api/webhooks/stripe
```

### Error Handling

```python
try:
    payment_intent = await stripe_adapter.create_payment_intent(
        amount=1000,
        currency='usd'
    )
except Exception as e:
    # Handle specific Stripe errors
    if 'insufficient_funds' in str(e):
        # Handle insufficient funds
        pass
    elif 'card_declined' in str(e):
        # Handle declined card
        pass
    else:
        # Handle other errors
        pass
```

### Idempotency

```python
# Use idempotency keys to prevent duplicate charges
payment_intent = await stripe_adapter.create_payment_intent(
    amount=1000,
    currency='usd',
    metadata={
        'idempotency_key': 'unique_order_id_123'
    }
)
```

## Common Use Cases

### E-commerce Checkout
1. Create Payment Intent on server
2. Collect payment on client with Stripe.js
3. Confirm payment
4. Handle webhook for fulfillment

### SaaS Subscriptions
1. Create Products and Prices
2. Display pricing table
3. Create Customer on signup
4. Create Subscription
5. Handle billing via webhooks

### Marketplace/Platform
1. Use Stripe Connect for multi-party payments
2. Create Connected Accounts
3. Handle platform fees
4. Manage payouts

### Recurring Billing
1. Create subscription with trial
2. Handle payment failures
3. Update billing
4. Provide customer portal

## Testing Scenarios

### Test Successful Payment
```python
# Use test mode
payment_intent = await stripe_adapter.create_payment_intent(
    amount=1000,
    currency='usd'
)

# Use test card: 4242 4242 4242 4242
# Expiry: Any future date
# CVC: Any 3 digits
```

### Test Failed Payment
```python
# Use decline test card: 4000 0000 0000 0002
# Payment will be declined
```

### Test Subscription Lifecycle
```python
# Create subscription with trial
sub = await stripe_adapter.create_subscription(
    customer_id='cus_test',
    items=[{'price': 'price_test'}],
    trial_period_days=7
)

# Simulate trial end and first payment
# Update subscription
# Cancel subscription
```

## Resources

### Documentation
- [Stripe API Reference](https://stripe.com/docs/api)
- [Payment Intents Guide](https://stripe.com/docs/payments/payment-intents)
- [Subscriptions Guide](https://stripe.com/docs/billing/subscriptions/overview)
- [Webhooks Guide](https://stripe.com/docs/webhooks)

### Tools
- [Stripe Dashboard](https://dashboard.stripe.com/)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)
- [API Logs](https://dashboard.stripe.com/logs)
- [Test Mode](https://dashboard.stripe.com/test/dashboard)

### SDKs
- [Node.js](https://github.com/stripe/stripe-node)
- [Python](https://github.com/stripe/stripe-python)
- [Ruby](https://github.com/stripe/stripe-ruby)
- [PHP](https://github.com/stripe/stripe-php)
- [React](https://github.com/stripe/react-stripe-js)

### Support
- [Stripe Support](https://support.stripe.com/)
- [Community Forum](https://stripe.com/community)
- [Status Page](https://status.stripe.com/)

## Error Codes

Common Stripe error codes:
- `card_declined`: Card was declined
- `expired_card`: Card has expired
- `insufficient_funds`: Insufficient funds
- `incorrect_cvc`: CVC is incorrect
- `processing_error`: Error processing the card
- `rate_limit`: Too many requests

## Webhook Events

Key events to handle:
- `payment_intent.succeeded`: Payment succeeded
- `payment_intent.payment_failed`: Payment failed
- `customer.subscription.created`: Subscription created
- `customer.subscription.updated`: Subscription changed
- `customer.subscription.deleted`: Subscription canceled
- `invoice.paid`: Invoice paid
- `invoice.payment_failed`: Invoice payment failed
- `charge.refunded`: Charge refunded
- `customer.created`: Customer created
- `customer.updated`: Customer updated

## Compliance

### PCI Compliance
- Use Stripe.js or Elements to collect card data
- Never send card data to your server
- Use hosted Checkout for simplest compliance

### SCA (Strong Customer Authentication)
- Stripe handles SCA automatically with Payment Intents
- Support 3D Secure when required
- Save cards for future payments with proper authentication

### Data Protection
- Use Stripe's tokenization
- Don't store raw card data
- Comply with GDPR for customer data
- Implement data retention policies

## Migration Guide

### From PayPal
1. Map PayPal products to Stripe products
2. Migrate customer data to Stripe customers
3. Update payment forms to use Stripe.js
4. Replace IPN with Stripe webhooks
5. Test thoroughly before switching

### From Other Processors
1. Export customer and subscription data
2. Create matching products in Stripe
3. Import customers with payment methods
4. Recreate active subscriptions
5. Set up webhooks
6. Gradually migrate traffic

## Performance Tips

- **Cache Products**: Cache product and price lists
- **Webhook Queue**: Process webhooks asynchronously
- **Pagination**: Use pagination for large lists
- **Expand Objects**: Use `expand` parameter to reduce API calls
- **Batch Operations**: Use batch APIs when available

## Support and Troubleshooting

### Common Issues

**Payment Failing**
- Check test vs live mode
- Verify API keys are correct
- Check card is not declined test card
- Review error messages in dashboard

**Webhook Not Received**
- Verify endpoint URL is accessible
- Check webhook signature verification
- Review webhook logs in dashboard
- Test with Stripe CLI

**Subscription Not Created**
- Ensure customer has payment method
- Check payment method is attached
- Verify price ID is correct
- Review error response

### Getting Help
1. Check [Stripe Documentation](https://stripe.com/docs)
2. Review [API Reference](https://stripe.com/docs/api)
3. Use [Stripe Dashboard](https://dashboard.stripe.com/) logs
4. Contact [Stripe Support](https://support.stripe.com/)
5. Post in [Community Forum](https://stripe.com/community)

## Next Steps

1. Sign up for a Stripe account
2. Get your API keys
3. Install Stripe SDK
4. Implement basic payment flow
5. Set up webhooks
6. Test in test mode
7. Go live with live keys
8. Monitor in Stripe Dashboard
