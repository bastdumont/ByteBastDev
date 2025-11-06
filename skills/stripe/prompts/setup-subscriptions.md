# Setup Stripe Subscriptions

Implement a complete subscription billing system with the following specifications:

## Subscription Configuration
- **Billing Intervals**: {intervals} (monthly, yearly, etc.)
- **Tiers**: {tier_names} (Starter, Pro, Enterprise, etc.)
- **Trial Period**: {trial_days} days
- **Features per Tier**: {features_list}

## Requirements

### 1. Product & Price Setup
Create Stripe products and prices:

**Products**
```typescript
// Define subscription tiers
const products = [
  {
    name: 'Starter',
    description: 'Perfect for individuals',
    features: ['Feature 1', 'Feature 2']
  },
  {
    name: 'Pro',
    description: 'For growing teams',
    features: ['All Starter features', 'Feature 3', 'Feature 4']
  },
  {
    name: 'Enterprise',
    description: 'For large organizations',
    features: ['All Pro features', 'Feature 5', 'Custom support']
  }
];
```

**Prices**
- Monthly pricing for each tier
- Annual pricing (with discount)
- Usage-based pricing (if applicable)

### 2. Backend Implementation

**Subscription Endpoints**
```
POST /api/subscriptions/create
POST /api/subscriptions/update
POST /api/subscriptions/cancel
GET  /api/subscriptions/:customerId
POST /api/subscriptions/preview
```

**Webhook Handler** (`/api/webhooks/stripe`)
Handle subscription lifecycle events:
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.subscription.trial_will_end`
- `invoice.paid`
- `invoice.payment_failed`
- `invoice.upcoming`

### 3. Frontend Components

**Pricing Table Component**
```typescript
// Display available plans
<PricingTable
  plans={plans}
  billingPeriod={billingPeriod}
  onSelectPlan={handleSelectPlan}
  currentPlan={userSubscription?.plan}
/>
```

**Subscription Manager Component**
- Display current subscription
- Show next billing date
- Display payment method
- Allow plan upgrades/downgrades
- Enable subscription cancellation
- Show billing history

**Payment Method Manager**
- Add new payment method
- Update default payment method
- Remove payment method
- Display saved cards

### 4. Customer Portal Integration
Set up Stripe Customer Portal:
- Enable in Stripe Dashboard
- Configure allowed features
- Customize branding
- Generate portal sessions

```typescript
// Create portal session
const portalSession = await stripe.billingPortal.sessions.create({
  customer: customerId,
  return_url: 'https://example.com/account'
});
```

### 5. Subscription Logic

**Trial Handling**
- Start trial when creating subscription
- Send reminder before trial ends
- Handle trial-to-paid conversion
- Allow cancellation during trial

**Proration**
- Calculate prorated charges for upgrades
- Handle downgrades at period end
- Display proration preview
- Apply credits correctly

**Failed Payments**
- Retry failed payments automatically
- Send dunning emails
- Implement grace period
- Cancel after retries exhausted

### 6. Database Schema
```sql
-- Subscriptions table
CREATE TABLE subscriptions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  stripe_customer_id VARCHAR(255),
  stripe_subscription_id VARCHAR(255),
  stripe_price_id VARCHAR(255),
  status VARCHAR(50),
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  cancel_at_period_end BOOLEAN,
  canceled_at TIMESTAMP,
  trial_end TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Invoices table
CREATE TABLE invoices (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  stripe_invoice_id VARCHAR(255),
  stripe_subscription_id VARCHAR(255),
  amount_paid INTEGER,
  currency VARCHAR(3),
  status VARCHAR(50),
  invoice_pdf VARCHAR(500),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 7. Email Notifications
Set up transactional emails for:
- Subscription created
- Trial ending soon
- Successful payment
- Failed payment
- Subscription canceled
- Plan upgraded/downgraded
- Invoice available

### 8. Usage Tracking (Optional)
If using usage-based billing:
- Track usage metrics
- Report usage to Stripe
- Display usage in dashboard
- Show usage limits
- Alert on approaching limits

## File Structure
```
src/
  ├── components/
  │   ├── subscription/
  │   │   ├── PricingTable.tsx
  │   │   ├── SubscriptionManager.tsx
  │   │   ├── PaymentMethodManager.tsx
  │   │   ├── BillingHistory.tsx
  │   │   └── PlanComparison.tsx
  │   └── checkout/
  │       └── SubscriptionCheckout.tsx
  ├── hooks/
  │   ├── useSubscription.ts
  │   ├── usePaymentMethods.ts
  │   └── useInvoices.ts
  ├── lib/
  │   ├── stripe.ts
  │   └── subscription-helpers.ts
  ├── api/
  │   ├── subscriptions/
  │   │   ├── create.ts
  │   │   ├── update.ts
  │   │   ├── cancel.ts
  │   │   └── preview.ts
  │   └── webhooks/
  │       └── stripe.ts
  └── types/
      └── subscription.ts
```

## Features to Implement

### Subscription Creation Flow
1. User selects plan
2. Create or retrieve Stripe customer
3. Collect payment method
4. Create subscription with trial (if applicable)
5. Redirect to success page
6. Send confirmation email

### Subscription Update Flow
1. User selects new plan
2. Calculate proration
3. Show preview of charges/credits
4. Confirm change
5. Update subscription
6. Update database
7. Send notification

### Subscription Cancellation Flow
1. User initiates cancellation
2. Offer retention incentives (optional)
3. Confirm cancellation
4. Cancel at period end or immediately
5. Update database
6. Send cancellation confirmation

### Payment Failure Flow
1. Payment fails
2. Send notification to user
3. Retry payment automatically
4. Mark subscription as past_due
5. After retries, cancel subscription
6. Notify user of cancellation

## Security & Best Practices
- Verify webhook signatures
- Use idempotency keys
- Handle race conditions
- Implement proper error handling
- Log all subscription events
- Secure API endpoints
- Validate user permissions
- Use environment variables for keys

## Testing Scenarios
- [ ] Create subscription with trial
- [ ] Trial ends and converts to paid
- [ ] Upgrade subscription mid-cycle
- [ ] Downgrade at period end
- [ ] Cancel immediately
- [ ] Cancel at period end
- [ ] Payment succeeds
- [ ] Payment fails and retries
- [ ] Update payment method
- [ ] View billing history
- [ ] Generate invoice PDF
- [ ] Handle webhook events

## Monitoring & Analytics
Track key metrics:
- MRR (Monthly Recurring Revenue)
- Churn rate
- Trial conversion rate
- Failed payment rate
- Customer lifetime value
- Active subscriptions
- Subscription distribution by plan

Generate all code, database schemas, and documentation.
