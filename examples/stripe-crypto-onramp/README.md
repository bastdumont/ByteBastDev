# Stripe Fiat-to-Crypto Onramp

A production-ready application for converting fiat currency to cryptocurrency using Stripe payments. Built with Next.js, TypeScript, Stripe API, and blockchain integration.

## Features

- 💳 **Stripe Payment Integration** - Accept credit cards, debit cards, and bank transfers
- 🪙 **Multi-Crypto Support** - Bitcoin, Ethereum, USDC, USDT, and more
- 🔐 **KYC/AML Compliance** - Identity verification and compliance checks
- 💱 **Real-time Exchange Rates** - Live crypto pricing with minimal slippage
- 🔒 **Secure Wallet Integration** - Support for multiple wallet types
- 📊 **Transaction History** - Complete audit trail of all transactions
- 🚀 **Fast Processing** - Quick fiat-to-crypto conversion
- 🌍 **Multi-Currency Support** - USD, EUR, GBP, and more
- 📱 **Mobile Responsive** - Works on all devices
- ⚡ **Real-time Updates** - WebSocket-based transaction status

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Stripe Elements** - Secure payment forms
- **Web3.js / Ethers.js** - Blockchain interaction
- **React Query** - Data fetching and caching

### Backend
- **Next.js API Routes** - Serverless functions
- **Stripe API** - Payment processing
- **Prisma** - Database ORM
- **PostgreSQL** - Database
- **Redis** - Caching and rate limiting
- **Blockchain APIs** - Crypto transactions

### Infrastructure
- **Vercel** - Deployment
- **AWS S3** - KYC document storage
- **CloudWatch** - Monitoring
- **Sentry** - Error tracking

## Quick Start

### Prerequisites

- Node.js 18+
- PostgreSQL database
- Redis instance
- Stripe account
- Blockchain node access (or third-party API)
- KYC provider account (optional)

### Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd stripe-crypto-onramp
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
```

4. Configure your `.env.local`:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/crypto_onramp

# Redis
REDIS_URL=redis://localhost:6379

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Crypto
ETHEREUM_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/...
BITCOIN_RPC_URL=...
CRYPTO_HOT_WALLET_PRIVATE_KEY=...

# Exchange Rate API
COINGECKO_API_KEY=...

# KYC Provider
KYC_PROVIDER_API_KEY=...

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000
```

5. Set up database:
```bash
npx prisma migrate dev
npx prisma db seed
```

6. Start development server:
```bash
npm run dev
```

7. Open [http://localhost:3000](http://localhost:3000)

## Project Structure

```
stripe-crypto-onramp/
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js app directory
│   │   │   ├── api/               # API routes
│   │   │   ├── onramp/            # Onramp pages
│   │   │   ├── transactions/      # Transaction history
│   │   │   └── kyc/               # KYC verification
│   │   ├── components/
│   │   │   ├── onramp/            # Onramp UI components
│   │   │   ├── wallet/            # Wallet components
│   │   │   └── ui/                # Shared UI components
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── lib/                   # Utilities
│   │   └── types/                 # TypeScript types
│   └── public/                    # Static assets
├── backend/
│   ├── api/
│   │   ├── payments/              # Stripe payment handlers
│   │   ├── crypto/                # Crypto transaction handlers
│   │   ├── webhooks/              # Webhook handlers
│   │   └── kyc/                   # KYC verification
│   ├── lib/                       # Backend utilities
│   └── models/                    # Data models
├── database/
│   ├── migrations/                # Prisma migrations
│   ├── schema.prisma              # Database schema
│   └── seed.ts                    # Seed data
└── config/                        # Configuration files
```

## Features in Detail

### 1. Payment Processing

**Supported Payment Methods:**
- Credit/Debit Cards (Visa, Mastercard, Amex)
- Bank Transfers (ACH, SEPA)
- Digital Wallets (Apple Pay, Google Pay)

**Payment Flow:**
1. User selects fiat amount and cryptocurrency
2. System calculates crypto amount based on current rates
3. User completes KYC (if required)
4. User enters payment details via Stripe
5. Payment is processed
6. Crypto is sent to user's wallet

### 2. Cryptocurrency Support

**Supported Cryptocurrencies:**
- Bitcoin (BTC)
- Ethereum (ETH)
- USD Coin (USDC)
- Tether (USDT)
- More via configuration

**Transaction Types:**
- Spot conversion (immediate)
- Scheduled conversion (future date)
- Recurring purchases (DCA)

### 3. KYC/AML Compliance

**Verification Levels:**

**Level 1 (No KYC)** - Limited
- Max: $100 per transaction
- Max: $500 per month
- Email verification only

**Level 2 (Basic KYC)** - Standard
- Max: $1,000 per transaction
- Max: $10,000 per month
- ID verification required

**Level 3 (Enhanced KYC)** - Premium
- Max: $10,000 per transaction
- Max: $100,000 per month
- ID + address verification
- Source of funds documentation

**KYC Process:**
1. Submit personal information
2. Upload government ID
3. Selfie verification
4. Address proof (utility bill)
5. Automated verification
6. Manual review (if needed)

### 4. Exchange Rate Calculation

**Rate Sources:**
- CoinGecko API
- CoinMarketCap API
- Binance API
- Average of multiple sources

**Pricing Formula:**
```
Crypto Amount = (Fiat Amount - Fees) / Exchange Rate
```

**Fees Structure:**
- Payment processing: 2.9% + $0.30 (Stripe)
- Platform fee: 1-3% (based on volume)
- Network fee: Variable (blockchain gas)

### 5. Wallet Integration

**Supported Wallets:**
- MetaMask
- WalletConnect
- Coinbase Wallet
- Manual address entry

**Security:**
- User addresses are validated
- Test transactions for new addresses
- Multi-signature for large amounts
- Cold storage for reserves

### 6. Transaction States

```
Pending → Payment Processing → Payment Confirmed →
Crypto Purchasing → Crypto Sending → Completed

Failed states:
- Payment Failed
- KYC Required
- Insufficient Liquidity
- Transaction Error
```

## API Documentation

### Create Onramp Transaction

```typescript
POST /api/onramp/create

Request:
{
  "fiatAmount": 100,
  "fiatCurrency": "USD",
  "cryptoCurrency": "ETH",
  "walletAddress": "0x123...",
  "paymentMethodId": "pm_123..."
}

Response:
{
  "transactionId": "txn_123",
  "status": "pending",
  "cryptoAmount": "0.045",
  "exchangeRate": 2200,
  "fees": {
    "stripe": 3.20,
    "platform": 2.00,
    "network": 1.50
  },
  "estimatedDelivery": "2024-11-06T10:30:00Z"
}
```

### Get Exchange Rate

```typescript
GET /api/rates/:cryptoCurrency?fiatCurrency=USD&amount=100

Response:
{
  "cryptoCurrency": "ETH",
  "fiatCurrency": "USD",
  "rate": 2200,
  "cryptoAmount": "0.045",
  "timestamp": "2024-11-06T10:00:00Z",
  "validUntil": "2024-11-06T10:05:00Z"
}
```

### Get Transaction Status

```typescript
GET /api/transactions/:id

Response:
{
  "id": "txn_123",
  "status": "completed",
  "fiatAmount": 100,
  "cryptoAmount": "0.045",
  "cryptoCurrency": "ETH",
  "walletAddress": "0x123...",
  "txHash": "0xabc...",
  "createdAt": "2024-11-06T10:00:00Z",
  "completedAt": "2024-11-06T10:15:00Z"
}
```

### Submit KYC

```typescript
POST /api/kyc/submit

Request (multipart/form-data):
{
  "firstName": "John",
  "lastName": "Doe",
  "dateOfBirth": "1990-01-01",
  "country": "US",
  "documentType": "passport",
  "documentFront": <file>,
  "documentBack": <file>,
  "selfie": <file>
}

Response:
{
  "kycId": "kyc_123",
  "status": "pending",
  "estimatedCompletion": "2024-11-06T12:00:00Z"
}
```

## Webhooks

### Stripe Payment Webhooks

```typescript
POST /api/webhooks/stripe

Events:
- payment_intent.succeeded
- payment_intent.payment_failed
- charge.refunded
```

### Blockchain Webhooks

```typescript
POST /api/webhooks/blockchain

Events:
- transaction.confirmed
- transaction.failed
- block.mined
```

## Database Schema

```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  kyc_level INTEGER DEFAULT 0,
  kyc_status VARCHAR(50),
  stripe_customer_id VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Transactions
CREATE TABLE transactions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  status VARCHAR(50) NOT NULL,
  fiat_amount DECIMAL(10,2) NOT NULL,
  fiat_currency VARCHAR(3) NOT NULL,
  crypto_amount DECIMAL(18,8) NOT NULL,
  crypto_currency VARCHAR(10) NOT NULL,
  wallet_address VARCHAR(255) NOT NULL,
  exchange_rate DECIMAL(18,8) NOT NULL,
  stripe_payment_intent_id VARCHAR(255),
  tx_hash VARCHAR(255),
  fees JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP
);

-- KYC Verifications
CREATE TABLE kyc_verifications (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  level INTEGER NOT NULL,
  status VARCHAR(50) NOT NULL,
  documents JSONB,
  verified_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Exchange Rates (cache)
CREATE TABLE exchange_rates (
  crypto_currency VARCHAR(10) NOT NULL,
  fiat_currency VARCHAR(3) NOT NULL,
  rate DECIMAL(18,8) NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  PRIMARY KEY (crypto_currency, fiat_currency, timestamp)
);
```

## Security

### Payment Security
- PCI-DSS compliant (via Stripe)
- No credit card data stored
- Stripe Elements for secure input
- 3D Secure authentication

### Crypto Security
- Hot wallet for transactions
- Cold storage for reserves
- Multi-signature for large amounts
- Address validation
- Transaction monitoring

### API Security
- Rate limiting
- JWT authentication
- CSRF protection
- Input validation
- SQL injection prevention

### Data Security
- Encryption at rest
- Encryption in transit (TLS)
- KYC documents in S3 with encryption
- Regular security audits
- GDPR compliance

## Compliance

### Regulations
- **KYC/AML** - Know Your Customer / Anti-Money Laundering
- **BSA** - Bank Secrecy Act (US)
- **MiCA** - Markets in Crypto-Assets (EU)
- **FinCEN** - Financial Crimes Enforcement Network

### Reporting
- Suspicious Activity Reports (SAR)
- Currency Transaction Reports (CTR)
- Transaction monitoring
- Audit logs

### Licenses Required
- Money Transmitter License (US state-by-state)
- Payment Institution License (EU)
- Cryptocurrency Exchange License (varies by jurisdiction)

## Testing

### Test Mode

Use Stripe test mode for development:

**Test Cards:**
- Success: 4242 4242 4242 4242
- Decline: 4000 0000 0000 0002
- 3D Secure: 4000 0027 6000 3184

**Test Blockchain:**
- Use testnets (Goerli, Sepolia for Ethereum)
- Bitcoin testnet
- Faucets for test funds

### Testing Scenarios

```bash
# Run unit tests
npm run test

# Run integration tests
npm run test:integration

# Run e2e tests
npm run test:e2e

# Test coverage
npm run test:coverage
```

## Deployment

### Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Environment Variables

Set in Vercel dashboard:
- All `.env` variables
- Production API keys
- Database connection strings
- Redis URL

### Database Migration

```bash
# Production migration
npx prisma migrate deploy
```

## Monitoring

### Metrics to Track
- Transaction volume
- Success rate
- Average processing time
- Fee revenue
- User acquisition
- KYC completion rate

### Alerts
- Failed payments
- Failed crypto transactions
- High error rates
- Unusual transaction patterns
- Security incidents

## Limitations

### Current Limitations
- Single currency per transaction
- No partial fills
- Limited to supported cryptocurrencies
- Geographic restrictions apply
- Transaction limits based on KYC level

### Future Enhancements
- Multi-crypto portfolios
- Recurring buys (DCA)
- Instant withdrawals
- Mobile app
- More payment methods
- More cryptocurrencies
- Advanced trading features

## Support

### Documentation
- [API Documentation](./docs/api.md)
- [Integration Guide](./docs/integration.md)
- [Security Best Practices](./docs/security.md)

### Help
- Email: support@example.com
- Discord: [Join our server](https://discord.gg/...)
- Twitter: [@example](https://twitter.com/example)

## License

MIT License - See LICENSE file for details

## Legal Disclaimer

This software is provided for educational purposes. Operating a fiat-to-crypto onramp requires proper licensing and compliance with local regulations. Consult with legal counsel before deploying in production.

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) first.

## Acknowledgments

- Stripe for payment processing
- CoinGecko for exchange rates
- Alchemy for blockchain infrastructure
- Vercel for hosting
