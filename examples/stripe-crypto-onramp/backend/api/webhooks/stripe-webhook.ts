/**
 * Stripe Webhook Handler
 * Processes payment lifecycle events and triggers crypto transactions
 */

import Stripe from 'stripe';
import { NextRequest, NextResponse } from 'next/server';
import { sendCrypto, monitorTransaction } from '../crypto/send-crypto';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

export async function POST(req: NextRequest) {
  const body = await req.text();
  const signature = req.headers.get('stripe-signature')!;

  let event: Stripe.Event;

  try {
    // Verify webhook signature
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );

  } catch (err: any) {
    console.error('⚠️  Webhook signature verification failed:', err.message);
    return NextResponse.json(
      { error: 'Webhook signature verification failed' },
      { status: 400 }
    );
  }

  console.log(`📨 Received event: ${event.type}`);

  try {
    // Route event to appropriate handler
    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentSucceeded(event.data.object as Stripe.PaymentIntent);
        break;

      case 'payment_intent.payment_failed':
        await handlePaymentFailed(event.data.object as Stripe.PaymentIntent);
        break;

      case 'charge.refunded':
        await handleChargeRefunded(event.data.object as Stripe.Charge);
        break;

      case 'charge.dispute.created':
        await handleDisputeCreated(event.data.object as Stripe.Dispute);
        break;

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    // Log successful processing
    await logWebhookEvent(event.id, event.type, 'success');

    return NextResponse.json({ received: true });

  } catch (error: any) {
    console.error(`Error processing ${event.type}:`, error);
    await logWebhookEvent(event.id, event.type, 'failed', error.message);

    // Return 500 so Stripe retries
    return NextResponse.json(
      { error: 'Webhook processing failed' },
      { status: 500 }
    );
  }
}

/**
 * Handle successful payment
 */
async function handlePaymentSucceeded(paymentIntent: Stripe.PaymentIntent) {
  const { transactionId, cryptoCurrency, cryptoAmount, walletAddress } =
    paymentIntent.metadata;

  console.log(`✅ Payment succeeded for transaction ${transactionId}`);

  try {
    // Update transaction status
    await updateTransaction(transactionId, {
      status: 'payment_confirmed',
      stripePaymentIntentId: paymentIntent.id
    });

    // Send notification
    await sendNotification(transactionId, 'payment_confirmed', {
      amount: paymentIntent.amount / 100,
      currency: paymentIntent.currency
    });

    // Initiate crypto transfer
    const cryptoTx = await sendCrypto({
      cryptoCurrency,
      amount: cryptoAmount,
      toAddress: walletAddress,
      transactionId
    });

    // Update transaction with crypto tx hash
    await updateTransaction(transactionId, {
      status: 'crypto_sent',
      txHash: cryptoTx.txHash
    });

    // Start monitoring confirmations
    const requiredConfirmations = cryptoCurrency === 'BTC' ? 6 : 12;
    monitorTransaction(cryptoTx.txHash, cryptoCurrency, requiredConfirmations)
      .catch(err => console.error('Error monitoring transaction:', err));

    // Send confirmation email
    await sendEmail(transactionId, 'crypto_sent', {
      txHash: cryptoTx.txHash,
      cryptoAmount,
      cryptoCurrency,
      walletAddress
    });

  } catch (error: any) {
    console.error('Error processing successful payment:', error);

    // Mark transaction as failed
    await updateTransaction(transactionId, {
      status: 'failed',
      failureReason: error.message
    });

    // Initiate refund
    await initiateRefund(paymentIntent.id, 'crypto_transaction_failed');
  }
}

/**
 * Handle failed payment
 */
async function handlePaymentFailed(paymentIntent: Stripe.PaymentIntent) {
  const { transactionId } = paymentIntent.metadata;

  console.log(`❌ Payment failed for transaction ${transactionId}`);

  const failureReason = paymentIntent.last_payment_error?.message || 'Payment failed';

  await updateTransaction(transactionId, {
    status: 'payment_failed',
    failureReason
  });

  await sendNotification(transactionId, 'payment_failed', {
    reason: failureReason
  });

  await sendEmail(transactionId, 'payment_failed', {
    reason: failureReason
  });
}

/**
 * Handle charge refund
 */
async function handleChargeRefunded(charge: Stripe.Charge) {
  const paymentIntent = charge.payment_intent as string;

  // Find transaction by payment intent
  const transaction = await findTransactionByPaymentIntent(paymentIntent);

  if (!transaction) {
    console.error(`Transaction not found for payment intent ${paymentIntent}`);
    return;
  }

  console.log(`💸 Refund processed for transaction ${transaction.id}`);

  await updateTransaction(transaction.id, {
    status: 'refunded'
  });

  await sendNotification(transaction.id, 'refunded', {
    amount: charge.amount_refunded / 100,
    currency: charge.currency
  });

  await sendEmail(transaction.id, 'refunded', {
    amount: charge.amount_refunded / 100,
    currency: charge.currency
  });
}

/**
 * Handle dispute created
 */
async function handleDisputeCreated(dispute: Stripe.Dispute) {
  const charge = dispute.charge as string;

  console.log(`⚠️  Dispute created for charge ${charge}`);

  // Find transaction
  const transaction = await findTransactionByCharge(charge);

  if (!transaction) {
    console.error(`Transaction not found for charge ${charge}`);
    return;
  }

  // Log dispute for manual review
  await logDispute({
    transactionId: transaction.id,
    disputeId: dispute.id,
    amount: dispute.amount,
    reason: dispute.reason,
    status: dispute.status
  });

  // Alert support team
  await alertSupport('dispute_created', {
    transactionId: transaction.id,
    disputeId: dispute.id,
    amount: dispute.amount / 100,
    reason: dispute.reason
  });
}

/**
 * Initiate refund
 */
async function initiateRefund(
  paymentIntentId: string,
  reason: string
): Promise<void> {
  try {
    const refund = await stripe.refunds.create({
      payment_intent: paymentIntentId,
      reason: 'requested_by_customer',
      metadata: {
        reason
      }
    });

    console.log(`Refund initiated: ${refund.id}`);

  } catch (error: any) {
    console.error('Error initiating refund:', error);
    throw error;
  }
}

/**
 * Update transaction in database
 */
async function updateTransaction(
  transactionId: string,
  updates: Record<string, any>
): Promise<void> {
  // Placeholder - implement actual database update
  console.log(`Updating transaction ${transactionId}:`, updates);
}

/**
 * Find transaction by payment intent
 */
async function findTransactionByPaymentIntent(
  paymentIntentId: string
): Promise<any> {
  // Placeholder - implement actual database query
  return { id: 'txn_123', stripePaymentIntentId: paymentIntentId };
}

/**
 * Find transaction by charge
 */
async function findTransactionByCharge(chargeId: string): Promise<any> {
  // Placeholder - implement actual database query
  return { id: 'txn_123' };
}

/**
 * Send notification to user
 */
async function sendNotification(
  transactionId: string,
  event: string,
  data: any
): Promise<void> {
  // Placeholder - implement notification system
  // Could use WebSockets, Push notifications, etc.
  console.log(`Sending notification for ${transactionId}:`, event, data);
}

/**
 * Send email to user
 */
async function sendEmail(
  transactionId: string,
  template: string,
  data: any
): Promise<void> {
  // Placeholder - implement email service (SendGrid, AWS SES, etc.)
  console.log(`Sending email for ${transactionId}:`, template, data);
}

/**
 * Log webhook event
 */
async function logWebhookEvent(
  eventId: string,
  eventType: string,
  status: 'success' | 'failed',
  error?: string
): Promise<void> {
  // Placeholder - implement webhook logging
  console.log(`Webhook event ${eventId} (${eventType}): ${status}`, error);
}

/**
 * Log dispute
 */
async function logDispute(dispute: any): Promise<void> {
  // Placeholder - implement dispute logging
  console.log('Dispute logged:', dispute);
}

/**
 * Alert support team
 */
async function alertSupport(event: string, data: any): Promise<void> {
  // Placeholder - implement support alerting (Slack, PagerDuty, etc.)
  console.log(`Support alert: ${event}`, data);
}
