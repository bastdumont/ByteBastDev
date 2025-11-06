'use client';

/**
 * Crypto Onramp Widget
 * Main component for fiat-to-crypto conversion
 */

import { useState, useEffect } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { CryptoSelector } from './CryptoSelector';
import { WalletAddressInput } from './WalletAddressInput';
import { ExchangeRateDisplay } from './ExchangeRateDisplay';
import { FeeBreakdown } from './FeeBreakdown';
import { TransactionSummary } from './TransactionSummary';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

interface OnrampWidgetProps {
  userId: string;
  kycLevel?: number;
  onSuccess?: (transactionId: string) => void;
  onError?: (error: string) => void;
}

export function OnrampWidget({ userId, kycLevel = 0, onSuccess, onError }: OnrampWidgetProps) {
  const [step, setStep] = useState<'amount' | 'wallet' | 'payment' | 'processing'>('amount');
  const [fiatAmount, setFiatAmount] = useState<string>('100');
  const [fiatCurrency, setFiatCurrency] = useState<string>('USD');
  const [cryptoCurrency, setCryptoCurrency] = useState<string>('ETH');
  const [walletAddress, setWalletAddress] = useState<string>('');
  const [exchangeRate, setExchangeRate] = useState<any>(null);
  const [clientSecret, setClientSecret] = useState<string>('');
  const [transactionId, setTransactionId] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  // Fetch exchange rate when amount or currency changes
  useEffect(() => {
    if (fiatAmount && parseFloat(fiatAmount) > 0) {
      fetchExchangeRate();
    }
  }, [fiatAmount, cryptoCurrency, fiatCurrency]);

  async function fetchExchangeRate() {
    try {
      const response = await fetch(
        `/api/rates/${cryptoCurrency}?fiatCurrency=${fiatCurrency}&amount=${fiatAmount}`
      );

      if (!response.ok) throw new Error('Failed to fetch exchange rate');

      const data = await response.json();
      setExchangeRate(data);

    } catch (err: any) {
      setError('Failed to fetch exchange rate');
      console.error(err);
    }
  }

  async function handleAmountNext() {
    const amount = parseFloat(fiatAmount);

    // Validate amount based on KYC level
    const limits = {
      0: { max: 100, label: 'No KYC' },
      1: { max: 1000, label: 'Basic KYC' },
      2: { max: 10000, label: 'Enhanced KYC' }
    };

    const limit = limits[kycLevel as keyof typeof limits];

    if (amount > limit.max) {
      setError(`Maximum ${limit.label} limit is $${limit.max}. Please complete ${
        kycLevel === 0 ? 'Basic' : 'Enhanced'
      } KYC to increase your limit.`);
      return;
    }

    if (amount < 10) {
      setError('Minimum amount is $10');
      return;
    }

    setError('');
    setStep('wallet');
  }

  async function handleWalletNext() {
    if (!walletAddress) {
      setError('Please enter a wallet address');
      return;
    }

    // Validate wallet address format
    const isValid = await validateWalletAddress(walletAddress, cryptoCurrency);

    if (!isValid) {
      setError('Invalid wallet address');
      return;
    }

    setError('');
    await createPaymentIntent();
  }

  async function createPaymentIntent() {
    setLoading(true);

    try {
      const response = await fetch('/api/payments/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fiatAmount: parseFloat(fiatAmount),
          fiatCurrency,
          cryptoCurrency,
          walletAddress,
          userId
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to create payment');
      }

      const data = await response.json();

      setClientSecret(data.clientSecret);
      setTransactionId(data.transactionId);
      setStep('payment');

    } catch (err: any) {
      setError(err.message);
      onError?.(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function validateWalletAddress(address: string, currency: string): Promise<boolean> {
    try {
      const response = await fetch('/api/crypto/validate-address', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address, currency })
      });

      const data = await response.json();
      return data.valid;

    } catch (err) {
      return false;
    }
  }

  function handleBack() {
    if (step === 'wallet') setStep('amount');
    if (step === 'payment') setStep('wallet');
  }

  return (
    <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-6">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Buy Crypto</h2>
        <p className="text-gray-600 mt-1">Convert fiat to cryptocurrency instantly</p>
      </div>

      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {['Amount', 'Wallet', 'Payment'].map((label, index) => {
            const stepIndex = ['amount', 'wallet', 'payment'].indexOf(step);
            const isActive = stepIndex >= index;
            const isCurrent = stepIndex === index;

            return (
              <div key={label} className="flex-1">
                <div className="flex items-center">
                  <div className={`
                    w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold
                    ${isActive ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'}
                    ${isCurrent ? 'ring-4 ring-blue-200' : ''}
                  `}>
                    {index + 1}
                  </div>
                  {index < 2 && (
                    <div className={`flex-1 h-1 mx-2 ${
                      stepIndex > index ? 'bg-blue-600' : 'bg-gray-200'
                    }`} />
                  )}
                </div>
                <div className="mt-2 text-xs text-center">{label}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800 text-sm">{error}</p>
        </div>
      )}

      {/* Step 1: Amount */}
      {step === 'amount' && (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              You pay
            </label>
            <div className="flex gap-2">
              <input
                type="number"
                value={fiatAmount}
                onChange={(e) => setFiatAmount(e.target.value)}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="100"
                min="10"
                step="0.01"
              />
              <select
                value={fiatCurrency}
                onChange={(e) => setFiatCurrency(e.target.value)}
                className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="USD">USD</option>
                <option value="EUR">EUR</option>
                <option value="GBP">GBP</option>
              </select>
            </div>
          </div>

          <CryptoSelector
            selected={cryptoCurrency}
            onChange={setCryptoCurrency}
          />

          {exchangeRate && (
            <>
              <ExchangeRateDisplay
                fiatAmount={parseFloat(fiatAmount)}
                fiatCurrency={fiatCurrency}
                cryptoCurrency={cryptoCurrency}
                rate={exchangeRate.rate}
                cryptoAmount={exchangeRate.cryptoAmount}
              />

              <FeeBreakdown
                fiatAmount={parseFloat(fiatAmount)}
                fees={calculateFees(parseFloat(fiatAmount))}
              />
            </>
          )}

          <button
            onClick={handleAmountNext}
            disabled={!fiatAmount || parseFloat(fiatAmount) < 10}
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
          >
            Continue
          </button>
        </div>
      )}

      {/* Step 2: Wallet Address */}
      {step === 'wallet' && (
        <div className="space-y-6">
          <TransactionSummary
            fiatAmount={parseFloat(fiatAmount)}
            fiatCurrency={fiatCurrency}
            cryptoAmount={exchangeRate?.cryptoAmount || '0'}
            cryptoCurrency={cryptoCurrency}
          />

          <WalletAddressInput
            currency={cryptoCurrency}
            value={walletAddress}
            onChange={setWalletAddress}
          />

          <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p className="text-sm text-yellow-800">
              ⚠️ <strong>Important:</strong> Please double-check your wallet address.
              Funds sent to an incorrect address cannot be recovered.
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleBack}
              className="flex-1 border border-gray-300 py-3 px-4 rounded-lg font-semibold hover:bg-gray-50 transition"
            >
              Back
            </button>
            <button
              onClick={handleWalletNext}
              disabled={!walletAddress || loading}
              className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
            >
              {loading ? 'Processing...' : 'Continue to Payment'}
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Payment */}
      {step === 'payment' && clientSecret && (
        <Elements stripe={stripePromise} options={{ clientSecret }}>
          <PaymentForm
            transactionId={transactionId}
            onSuccess={() => {
              setStep('processing');
              onSuccess?.(transactionId);
            }}
            onError={(err) => {
              setError(err);
              onError?.(err);
            }}
            onBack={handleBack}
          />
        </Elements>
      )}

      {/* Processing State */}
      {step === 'processing' && (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h3 className="text-lg font-semibold mb-2">Processing your transaction...</h3>
          <p className="text-gray-600">
            Your crypto will be sent to your wallet shortly.
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Transaction ID: {transactionId}
          </p>
        </div>
      )}
    </div>
  );
}

function PaymentForm({
  transactionId,
  onSuccess,
  onError,
  onBack
}: {
  transactionId: string;
  onSuccess: () => void;
  onError: (error: string) => void;
  onBack: () => void;
}) {
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!stripe || !elements) return;

    setLoading(true);

    try {
      const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: `${window.location.origin}/transactions/${transactionId}`,
        },
      });

      if (error) {
        throw new Error(error.message);
      }

      onSuccess();

    } catch (err: any) {
      onError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <PaymentElement />

      <div className="flex gap-3">
        <button
          type="button"
          onClick={onBack}
          className="flex-1 border border-gray-300 py-3 px-4 rounded-lg font-semibold hover:bg-gray-50 transition"
        >
          Back
        </button>
        <button
          type="submit"
          disabled={!stripe || loading}
          className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
        >
          {loading ? 'Processing...' : 'Pay Now'}
        </button>
      </div>
    </form>
  );
}

function calculateFees(amount: number) {
  const stripeFee = (amount * 0.029) + 0.30;
  const platformFee = Math.max((amount * 0.02), 1.00);
  const networkFee = 1.50;

  return {
    stripe: stripeFee,
    platform: platformFee,
    network: networkFee,
    total: stripeFee + platformFee + networkFee
  };
}
