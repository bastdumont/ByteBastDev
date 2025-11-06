# Setup Stripe Customer Portal

Implement self-service billing management with Stripe Customer Portal:

## Portal Configuration
- **Features**: {features} (payment methods, subscriptions, invoices, etc.)
- **Branding**: {branding_requirements}
- **Return URL**: {return_url}

## Requirements

### 1. Portal Session Creation

**Backend Endpoint** (`/api/create-portal-session`)
```typescript
POST /api/create-portal-session
{
  "customer_id": "cus_123",
  "return_url": "https://example.com/account"
}

Response:
{
  "url": "https://billing.stripe.com/session/..."
}
```

**Implementation**
```typescript
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const { customer_id, return_url } = await req.json();

  try {
    const session = await stripe.billingPortal.sessions.create({
      customer: customer_id,
      return_url: return_url || process.env.APP_URL + '/account'
    });

    return new Response(JSON.stringify({ url: session.url }), {
      status: 200
    });
  } catch (error) {
    return new Response(error.message, { status: 500 });
  }
}
```

### 2. Frontend Integration

**Portal Button Component**
```typescript
import { useState } from 'react';

export function ManageBillingButton({ customerId }: { customerId: string }) {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);

    try {
      const response = await fetch('/api/create-portal-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_id: customerId,
          return_url: window.location.href
        })
      });

      const { url } = await response.json();
      window.location.href = url;
    } catch (error) {
      console.error('Error creating portal session:', error);
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      className="btn-primary"
    >
      {loading ? 'Loading...' : 'Manage Billing'}
    </button>
  );
}
```

### 3. Dashboard Configuration

**Configure Portal in Stripe Dashboard**

Navigate to: Settings > Billing > Customer portal

**Enable Features:**
- ✅ Update payment methods
- ✅ Update subscriptions
- ✅ Cancel subscriptions
- ✅ View invoices
- ✅ View billing history

**Subscription Management:**
- Allow plan switching
- Configure cancellation behavior
- Set proration preferences
- Enable trial conversions
- Configure pause subscription

**Invoice Settings:**
- Show payment history
- Allow invoice downloads
- Display payment method

### 4. Branding Customization

**Configure Branding**
```typescript
// Via Stripe Dashboard or API
const configuration = await stripe.billingPortal.configurations.create({
  business_profile: {
    headline: 'Manage Your Subscription',
    privacy_policy_url: 'https://example.com/privacy',
    terms_of_service_url: 'https://example.com/terms'
  },
  features: {
    customer_update: {
      allowed_updates: ['email', 'address', 'phone'],
      enabled: true
    },
    invoice_history: {
      enabled: true
    },
    payment_method_update: {
      enabled: true
    },
    subscription_cancel: {
      enabled: true,
      mode: 'at_period_end',
      cancellation_reason: {
        enabled: true,
        options: [
          'too_expensive',
          'missing_features',
          'switched_service',
          'unused',
          'other'
        ]
      }
    },
    subscription_pause: {
      enabled: false
    },
    subscription_update: {
      enabled: true,
      default_allowed_updates: ['price', 'quantity'],
      proration_behavior: 'create_prorations'
    }
  }
});
```

### 5. Portal Features

**Payment Methods**
- Add new cards
- Set default payment method
- Remove payment methods
- Update billing details

**Subscriptions**
- View current plan
- Upgrade/downgrade plans
- Cancel subscription
- Resume canceled subscription
- Pause subscription (if enabled)
- Change billing cycle

**Invoices**
- View invoice history
- Download invoice PDFs
- See upcoming invoices
- View payment status

**Account Information**
- Update email address
- Update billing address
- Update phone number
- Update tax IDs

### 6. Portal URLs

**Session Types**
```typescript
// Standard portal
const session = await stripe.billingPortal.sessions.create({
  customer: 'cus_123',
  return_url: 'https://example.com/account'
});

// Portal with flow (future feature)
const sessionWithFlow = await stripe.billingPortal.sessions.create({
  customer: 'cus_123',
  return_url: 'https://example.com/account',
  flow_data: {
    type: 'subscription_cancel',
    subscription_cancel: {
      subscription: 'sub_123'
    }
  }
});
```

### 7. Integration in Account Page

**Account Dashboard**
```typescript
export function AccountDashboard({ user, subscription }) {
  return (
    <div className="account-page">
      <h1>Account Settings</h1>

      {/* Subscription Info */}
      <section className="subscription-section">
        <h2>Subscription</h2>
        <div className="subscription-info">
          <p>Plan: {subscription.plan_name}</p>
          <p>Status: {subscription.status}</p>
          <p>Next billing: {subscription.next_billing_date}</p>
        </div>

        <ManageBillingButton customerId={user.stripe_customer_id} />
      </section>

      {/* Account Info */}
      <section className="account-info">
        <h2>Account Information</h2>
        <p>Email: {user.email}</p>
        <p>Member since: {user.created_at}</p>
      </section>

      {/* Billing History */}
      <section className="billing-history">
        <h2>Billing History</h2>
        <InvoiceList invoices={user.invoices} />
        <ManageBillingButton customerId={user.stripe_customer_id} />
      </section>
    </div>
  );
}
```

### 8. Handle Portal Events

**Webhook Events**
```typescript
// Handle customer portal events
switch (event.type) {
  case 'customer.subscription.updated':
    // User changed subscription in portal
    await syncSubscription(event.data.object);
    break;

  case 'customer.subscription.deleted':
    // User canceled in portal
    await handleCancellation(event.data.object);
    break;

  case 'customer.updated':
    // User updated info in portal
    await syncCustomer(event.data.object);
    break;

  case 'payment_method.attached':
    // User added payment method in portal
    await syncPaymentMethod(event.data.object);
    break;
}
```

### 9. Security Considerations

**Authentication**
- Verify user owns the customer ID
- Require login before portal access
- Validate session on return
- Implement CSRF protection

```typescript
// Verify customer ownership
export async function POST(req: Request) {
  const session = await getSession(req);
  const { customer_id } = await req.json();

  // Verify this customer belongs to logged-in user
  const user = await db.users.findUnique({
    where: { id: session.user.id }
  });

  if (user.stripe_customer_id !== customer_id) {
    return new Response('Unauthorized', { status: 403 });
  }

  // Create portal session...
}
```

### 10. Testing

**Test Portal Flow**
- [ ] Access portal from account page
- [ ] Add new payment method
- [ ] Update payment method
- [ ] Remove payment method
- [ ] View invoices
- [ ] Download invoice PDF
- [ ] Change subscription plan
- [ ] Cancel subscription
- [ ] Return to application
- [ ] Verify changes in database

## File Structure
```
src/
  ├── components/
  │   ├── account/
  │   │   ├── AccountDashboard.tsx
  │   │   ├── ManageBillingButton.tsx
  │   │   ├── SubscriptionInfo.tsx
  │   │   └── InvoiceList.tsx
  │   └── subscription/
  │       └── PortalButton.tsx
  ├── api/
  │   ├── create-portal-session.ts
  │   └── webhooks/
  │       └── stripe.ts
  └── lib/
      └── stripe.ts
```

## Portal Configuration Options

**Subscription Cancellation**
- Immediate cancellation
- Cancel at period end
- Require cancellation reason
- Offer retention discounts
- Show downgrade options

**Plan Changes**
- Allowed plan changes
- Proration behavior
- Change restrictions
- Billing cycle alignment

**Payment Method Updates**
- Required for active subscriptions
- Allow multiple payment methods
- Set default payment method
- Collect billing address

## User Experience

**Portal Flow**
1. User clicks "Manage Billing"
2. Redirect to Stripe-hosted portal
3. User makes changes
4. Redirect back to application
5. Show confirmation message
6. Sync changes via webhook

**Return URL Handling**
```typescript
// On return from portal
export default function AccountPage() {
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);

    if (params.get('portal_return')) {
      // Show success message
      toast.success('Billing updated successfully');

      // Refresh data
      refreshSubscription();

      // Clean URL
      window.history.replaceState({}, '', '/account');
    }
  }, []);

  // ...
}
```

## Monitoring

**Track Portal Usage**
- Portal sessions created
- Features used
- Cancellation reasons
- Time spent in portal
- Completion rate

**Analytics Events**
```typescript
// Track portal access
analytics.track('portal_opened', {
  customer_id: customerId,
  source: 'account_page'
});

// Track return from portal
analytics.track('portal_returned', {
  customer_id: customerId,
  changes_made: true
});
```

## Best Practices

- ✅ Always verify customer ownership
- ✅ Use return_url for smooth UX
- ✅ Configure appropriate features
- ✅ Match your brand in portal
- ✅ Handle webhooks for sync
- ✅ Provide clear navigation
- ✅ Test all portal features
- ✅ Monitor usage and issues

Generate all necessary code and configuration.
