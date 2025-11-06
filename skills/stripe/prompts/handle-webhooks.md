# Setup Stripe Webhooks

Implement a robust webhook handler for Stripe events:

## Webhook Configuration
- **Endpoint URL**: {webhook_url}
- **Events to Handle**: {event_types}
- **Platform**: {platform} (Node.js, Python, etc.)

## Requirements

### 1. Webhook Endpoint Setup

**Create Endpoint** (`/api/webhooks/stripe`)
```typescript
POST /api/webhooks/stripe
Headers:
  stripe-signature: <signature>
Body:
  <raw JSON payload>
```

**Implementation Requirements**
- Accept POST requests only
- Receive raw request body
- Verify signature
- Process events asynchronously
- Return 200 status quickly
- Handle retries idempotently

### 2. Signature Verification

**Verify Webhook Signature**
```typescript
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const body = await req.text();
  const signature = req.headers.get('stripe-signature')!;

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    console.error('⚠️  Webhook signature verification failed:', err.message);
    return new Response('Webhook signature verification failed', {
      status: 400
    });
  }

  // Process event
  await handleEvent(event);

  return new Response(JSON.stringify({ received: true }), {
    status: 200
  });
}
```

### 3. Event Handlers

**Payment Events**
```typescript
async function handlePaymentIntentSucceeded(event: Stripe.Event) {
  const paymentIntent = event.data.object as Stripe.PaymentIntent;

  // Update order status
  await updateOrderStatus(
    paymentIntent.metadata.order_id,
    'paid'
  );

  // Send confirmation email
  await sendConfirmationEmail(
    paymentIntent.customer,
    paymentIntent.id
  );

  // Fulfill order
  await fulfillOrder(paymentIntent.metadata.order_id);
}

async function handlePaymentIntentFailed(event: Stripe.Event) {
  const paymentIntent = event.data.object as Stripe.PaymentIntent;

  // Update order status
  await updateOrderStatus(
    paymentIntent.metadata.order_id,
    'payment_failed'
  );

  // Notify customer
  await sendPaymentFailedEmail(
    paymentIntent.customer,
    paymentIntent.last_payment_error?.message
  );
}
```

**Subscription Events**
```typescript
async function handleSubscriptionCreated(event: Stripe.Event) {
  const subscription = event.data.object as Stripe.Subscription;

  // Create subscription record
  await createSubscription({
    userId: subscription.metadata.user_id,
    stripeSubscriptionId: subscription.id,
    stripeCustomerId: subscription.customer,
    status: subscription.status,
    currentPeriodEnd: new Date(subscription.current_period_end * 1000)
  });

  // Grant access
  await grantAccess(subscription.metadata.user_id);

  // Send welcome email
  await sendWelcomeEmail(subscription.customer);
}

async function handleSubscriptionUpdated(event: Stripe.Event) {
  const subscription = event.data.object as Stripe.Subscription;

  // Update subscription record
  await updateSubscription(subscription.id, {
    status: subscription.status,
    currentPeriodEnd: new Date(subscription.current_period_end * 1000),
    cancelAtPeriodEnd: subscription.cancel_at_period_end
  });

  // Handle status changes
  if (subscription.status === 'past_due') {
    await handlePastDue(subscription);
  } else if (subscription.status === 'canceled') {
    await revokeAccess(subscription.metadata.user_id);
  }
}

async function handleSubscriptionDeleted(event: Stripe.Event) {
  const subscription = event.data.object as Stripe.Subscription;

  // Update subscription record
  await updateSubscription(subscription.id, {
    status: 'canceled',
    canceledAt: new Date()
  });

  // Revoke access
  await revokeAccess(subscription.metadata.user_id);

  // Send cancellation confirmation
  await sendCancellationEmail(subscription.customer);
}
```

**Invoice Events**
```typescript
async function handleInvoicePaid(event: Stripe.Event) {
  const invoice = event.data.object as Stripe.Invoice;

  // Record payment
  await recordInvoicePayment({
    invoiceId: invoice.id,
    subscriptionId: invoice.subscription,
    amountPaid: invoice.amount_paid,
    paidAt: new Date(invoice.status_transitions.paid_at! * 1000)
  });

  // Send receipt
  await sendReceipt(invoice.customer, invoice.invoice_pdf);
}

async function handleInvoicePaymentFailed(event: Stripe.Event) {
  const invoice = event.data.object as Stripe.Invoice;

  // Log failed payment
  await logFailedPayment({
    invoiceId: invoice.id,
    subscriptionId: invoice.subscription,
    attemptCount: invoice.attempt_count
  });

  // Send dunning email
  await sendPaymentFailureEmail(
    invoice.customer,
    invoice.attempt_count
  );

  // Update subscription status
  if (invoice.subscription) {
    await updateSubscription(invoice.subscription as string, {
      status: 'past_due'
    });
  }
}

async function handleInvoiceUpcoming(event: Stripe.Event) {
  const invoice = event.data.object as Stripe.Invoice;

  // Send upcoming invoice notification
  await sendUpcomingInvoiceEmail(
    invoice.customer,
    invoice.amount_due,
    new Date(invoice.period_end * 1000)
  );
}
```

**Checkout Events**
```typescript
async function handleCheckoutSessionCompleted(event: Stripe.Event) {
  const session = event.data.object as Stripe.Checkout.Session;

  if (session.mode === 'payment') {
    // One-time payment
    await fulfillOrder(session.metadata?.order_id);
  } else if (session.mode === 'subscription') {
    // Subscription created via Checkout
    await grantSubscriptionAccess(
      session.metadata?.user_id,
      session.subscription as string
    );
  }

  // Send confirmation
  await sendCheckoutConfirmation(
    session.customer_email,
    session.id
  );
}
```

**Customer Events**
```typescript
async function handleCustomerCreated(event: Stripe.Event) {
  const customer = event.data.object as Stripe.Customer;

  // Sync customer to database
  await syncCustomer({
    stripeCustomerId: customer.id,
    email: customer.email,
    name: customer.name
  });
}

async function handleCustomerUpdated(event: Stripe.Event) {
  const customer = event.data.object as Stripe.Customer;

  // Update customer record
  await updateCustomer(customer.id, {
    email: customer.email,
    name: customer.name
  });
}
```

### 4. Event Router

**Route Events to Handlers**
```typescript
async function handleEvent(event: Stripe.Event) {
  console.log(`📨 Received event: ${event.type}`);

  try {
    switch (event.type) {
      // Payment events
      case 'payment_intent.succeeded':
        await handlePaymentIntentSucceeded(event);
        break;
      case 'payment_intent.payment_failed':
        await handlePaymentIntentFailed(event);
        break;

      // Subscription events
      case 'customer.subscription.created':
        await handleSubscriptionCreated(event);
        break;
      case 'customer.subscription.updated':
        await handleSubscriptionUpdated(event);
        break;
      case 'customer.subscription.deleted':
        await handleSubscriptionDeleted(event);
        break;
      case 'customer.subscription.trial_will_end':
        await handleTrialWillEnd(event);
        break;

      // Invoice events
      case 'invoice.paid':
        await handleInvoicePaid(event);
        break;
      case 'invoice.payment_failed':
        await handleInvoicePaymentFailed(event);
        break;
      case 'invoice.upcoming':
        await handleInvoiceUpcoming(event);
        break;

      // Checkout events
      case 'checkout.session.completed':
        await handleCheckoutSessionCompleted(event);
        break;
      case 'checkout.session.async_payment_succeeded':
        await handleAsyncPaymentSucceeded(event);
        break;
      case 'checkout.session.async_payment_failed':
        await handleAsyncPaymentFailed(event);
        break;

      // Customer events
      case 'customer.created':
        await handleCustomerCreated(event);
        break;
      case 'customer.updated':
        await handleCustomerUpdated(event);
        break;

      // Charge events
      case 'charge.refunded':
        await handleChargeRefunded(event);
        break;
      case 'charge.dispute.created':
        await handleDisputeCreated(event);
        break;

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    // Log successful processing
    await logWebhookEvent(event.id, event.type, 'success');

  } catch (error) {
    console.error(`Error processing ${event.type}:`, error);
    await logWebhookEvent(event.id, event.type, 'failed', error.message);
    throw error; // Stripe will retry
  }
}
```

### 5. Database Logging

**Log Webhook Events**
```typescript
async function logWebhookEvent(
  eventId: string,
  eventType: string,
  status: 'success' | 'failed',
  error?: string
) {
  await db.webhookLogs.create({
    data: {
      eventId,
      eventType,
      status,
      error,
      processedAt: new Date()
    }
  });
}
```

### 6. Idempotency

**Prevent Duplicate Processing**
```typescript
async function handleEvent(event: Stripe.Event) {
  // Check if event already processed
  const existing = await db.webhookLogs.findUnique({
    where: { eventId: event.id }
  });

  if (existing) {
    console.log(`Event ${event.id} already processed`);
    return;
  }

  // Process event...
}
```

### 7. Error Handling

**Retry Logic**
- Return 200 for successfully processed events
- Return 4xx for invalid requests (won't retry)
- Return 5xx for server errors (Stripe will retry)
- Implement exponential backoff

**Error Scenarios**
```typescript
try {
  await handleEvent(event);
} catch (error) {
  if (error.code === 'RECORD_NOT_FOUND') {
    // Don't retry - data issue
    console.error('Record not found:', error);
    return new Response('OK', { status: 200 });
  }

  // Retry on other errors
  throw error;
}
```

## File Structure
```
api/
  └── webhooks/
      ├── stripe.ts
      ├── handlers/
      │   ├── payment.ts
      │   ├── subscription.ts
      │   ├── invoice.ts
      │   ├── checkout.ts
      │   └── customer.ts
      └── utils/
          ├── logger.ts
          └── idempotency.ts
```

## Stripe Dashboard Configuration

1. **Add Webhook Endpoint**
   - Go to Developers > Webhooks
   - Click "Add endpoint"
   - Enter your URL: `https://yourdomain.com/api/webhooks/stripe`
   - Select events to listen for
   - Save and copy webhook secret

2. **Select Events**
   Payment events:
   - payment_intent.succeeded
   - payment_intent.payment_failed
   - charge.refunded

   Subscription events:
   - customer.subscription.created
   - customer.subscription.updated
   - customer.subscription.deleted
   - customer.subscription.trial_will_end

   Invoice events:
   - invoice.paid
   - invoice.payment_failed
   - invoice.upcoming

   Checkout events:
   - checkout.session.completed
   - checkout.session.async_payment_succeeded
   - checkout.session.async_payment_failed

## Testing Webhooks

**Use Stripe CLI**
```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger test events
stripe trigger payment_intent.succeeded
stripe trigger customer.subscription.created
stripe trigger invoice.payment_failed
```

**Test Event Handling**
```bash
# Send test event
curl -X POST http://localhost:3000/api/webhooks/stripe \
  -H "Content-Type: application/json" \
  -H "stripe-signature: test_signature" \
  -d @test_event.json
```

## Monitoring

**Track Webhook Health**
- Monitor processing time
- Track success/failure rates
- Alert on errors
- Review Stripe webhook logs
- Set up monitoring dashboards

**Key Metrics**
- Events received
- Events processed successfully
- Events failed
- Average processing time
- Retry rates

## Best Practices

- ✅ Always verify webhook signatures
- ✅ Return 200 status quickly
- ✅ Process events asynchronously
- ✅ Implement idempotency
- ✅ Log all events
- ✅ Handle retries gracefully
- ✅ Monitor webhook health
- ✅ Test thoroughly
- ✅ Use meaningful metadata
- ✅ Keep handlers focused

## Security

- Verify signatures on every request
- Use HTTPS only
- Store webhook secret securely
- Validate event data
- Rate limit endpoint
- Monitor for suspicious activity

Generate all webhook handler code and configuration.
