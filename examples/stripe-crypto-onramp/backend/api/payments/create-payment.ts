/**
 * Create Payment Intent for Fiat-to-Crypto Onramp
 */

import Stripe from 'stripe';
import { NextRequest, NextResponse } from 'next/server';
import { getExchangeRate } from '../crypto/exchange-rates';
import { validateTransaction, checkTransactionLimits } from '../../lib/validation';
import { getUserKYCLevel } from '../kyc/kyc-service';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

export interface CreatePaymentRequest {
  fiatAmount: number;
  fiatCurrency: string;
  cryptoCurrency: string;
  walletAddress: string;
  userId: string;
  paymentMethodId?: string;
}

export interface CreatePaymentResponse {
  paymentIntentId: string;
  clientSecret: string;
  transactionId: string;
  cryptoAmount: string;
  exchangeRate: number;
  fees: {
    stripe: number;
    platform: number;
    network: number;
    total: number;
  };
  estimatedDelivery: string;
}

export async function POST(req: NextRequest) {
  try {
    const body: CreatePaymentRequest = await req.json();
    const {
      fiatAmount,
      fiatCurrency,
      cryptoCurrency,
      walletAddress,
      userId,
      paymentMethodId
    } = body;

    // Validate input
    const validation = await validateTransaction({
      fiatAmount,
      fiatCurrency,
      cryptoCurrency,
      walletAddress
    });

    if (!validation.valid) {
      return NextResponse.json(
        { error: validation.error },
        { status: 400 }
      );
    }

    // Check user KYC level and transaction limits
    const kycLevel = await getUserKYCLevel(userId);
    const limitsCheck = await checkTransactionLimits(
      userId,
      fiatAmount,
      kycLevel
    );

    if (!limitsCheck.allowed) {
      return NextResponse.json(
        {
          error: limitsCheck.reason,
          kycLevel,
          currentLimit: limitsCheck.currentLimit,
          requiredLevel: limitsCheck.requiredLevel
        },
        { status: 403 }
      );
    }

    // Get current exchange rate
    const rateData = await getExchangeRate(cryptoCurrency, fiatCurrency);

    if (!rateData) {
      return NextResponse.json(
        { error: 'Unable to fetch exchange rate' },
        { status: 503 }
      );
    }

    // Calculate fees
    const stripeFee = (fiatAmount * 0.029) + 0.30; // 2.9% + $0.30
    const platformFeePercentage = parseFloat(process.env.PLATFORM_FEE_PERCENTAGE || '2.0');
    const platformFee = Math.max(
      (fiatAmount * platformFeePercentage) / 100,
      parseFloat(process.env.MIN_PLATFORM_FEE || '1.00')
    );

    // Network fee (estimated, will be calculated precisely later)
    const networkFee = cryptoCurrency === 'BTC' ? 2.50 : 1.50;

    const totalFees = stripeFee + platformFee + networkFee;
    const netAmount = fiatAmount - totalFees;

    // Calculate crypto amount
    const cryptoAmount = (netAmount / rateData.rate).toFixed(8);

    // Create transaction record in database
    const transaction = await prisma.transaction.create({
      data: {
        userId,
        status: 'pending',
        fiatAmount,
        fiatCurrency,
        cryptoAmount: parseFloat(cryptoAmount),
        cryptoCurrency,
        walletAddress,
        exchangeRate: rateData.rate,
        fees: {
          stripe: stripeFee,
          platform: platformFee,
          network: networkFee,
          total: totalFees
        }
      }
    });

    // Create Stripe Payment Intent
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(fiatAmount * 100), // Convert to cents
      currency: fiatCurrency.toLowerCase(),
      payment_method: paymentMethodId,
      confirmation_method: 'manual',
      capture_method: 'automatic',
      metadata: {
        transactionId: transaction.id,
        userId,
        cryptoCurrency,
        cryptoAmount,
        walletAddress,
        type: 'crypto_onramp'
      },
      description: `Purchase ${cryptoAmount} ${cryptoCurrency}`
    });

    // Update transaction with payment intent ID
    await prisma.transaction.update({
      where: { id: transaction.id },
      data: { stripePaymentIntentId: paymentIntent.id }
    });

    // Estimate delivery time (10-30 minutes)
    const estimatedDelivery = new Date(Date.now() + 20 * 60 * 1000).toISOString();

    const response: CreatePaymentResponse = {
      paymentIntentId: paymentIntent.id,
      clientSecret: paymentIntent.client_secret!,
      transactionId: transaction.id,
      cryptoAmount,
      exchangeRate: rateData.rate,
      fees: {
        stripe: stripeFee,
        platform: platformFee,
        network: networkFee,
        total: totalFees
      },
      estimatedDelivery
    };

    return NextResponse.json(response);

  } catch (error: any) {
    console.error('Error creating payment:', error);

    return NextResponse.json(
      {
        error: 'Failed to create payment',
        details: error.message
      },
      { status: 500 }
    );
  }
}

/**
 * Confirm Payment Intent
 */
export async function PATCH(req: NextRequest) {
  try {
    const { paymentIntentId, paymentMethodId } = await req.json();

    // Confirm the payment intent
    const paymentIntent = await stripe.paymentIntents.confirm(
      paymentIntentId,
      {
        payment_method: paymentMethodId
      }
    );

    // Update transaction status
    await prisma.transaction.update({
      where: { stripePaymentIntentId: paymentIntentId },
      data: { status: 'payment_processing' }
    });

    return NextResponse.json({
      status: paymentIntent.status,
      clientSecret: paymentIntent.client_secret
    });

  } catch (error: any) {
    console.error('Error confirming payment:', error);

    return NextResponse.json(
      {
        error: 'Failed to confirm payment',
        details: error.message
      },
      { status: 500 }
    );
  }
}

// Placeholder for Prisma client (should be imported from lib)
const prisma = {
  transaction: {
    create: async (data: any) => ({ id: 'txn_' + Math.random().toString(36).substr(2, 9), ...data.data }),
    update: async (params: any) => ({ ...params.data }),
    findUnique: async (params: any) => null
  }
};
