# Deployment Guide - Stripe Crypto Onramp

## Pre-Deployment Checklist

### 1. Environment Setup

✅ **Stripe Configuration**
- [ ] Create Stripe account (https://stripe.com)
- [ ] Get API keys (Dashboard > Developers > API keys)
- [ ] Set up webhook endpoint (Dashboard > Developers > Webhooks)
- [ ] Configure Stripe Checkout (Dashboard > Settings > Checkout)
- [ ] Enable payment methods (Cards, Apple Pay, Google Pay)

✅ **Database**
- [ ] Create PostgreSQL database
- [ ] Run migrations: `npx prisma migrate deploy`
- [ ] Seed initial data: `npm run db:seed`

✅ **Redis**
- [ ] Set up Redis instance (AWS ElastiCache, Redis Cloud, or local)
- [ ] Configure connection URL

✅ **Blockchain Infrastructure**
- [ ] Create Alchemy/Infura account for Ethereum RPC
- [ ] Set up Bitcoin node or use third-party service
- [ ] Generate hot wallet (for sending crypto)
- [ ] Set up cold wallet (for reserves)
- [ ] Fund hot wallet with initial crypto reserves

✅ **KYC Provider**
- [ ] Choose KYC provider (Onfido, Sumsub, etc.)
- [ ] Create account and get API keys
- [ ] Configure verification flows

✅ **AWS S3**
- [ ] Create S3 bucket for KYC documents
- [ ] Enable encryption
- [ ] Set up IAM user with S3 access
- [ ] Configure CORS if needed

✅ **Email Service**
- [ ] Set up SendGrid or AWS SES
- [ ] Verify sender domain
- [ ] Create email templates

✅ **Monitoring**
- [ ] Set up Sentry for error tracking
- [ ] Configure CloudWatch or similar

### 2. Security Checklist

- [ ] All private keys stored in environment variables
- [ ] Webhook secrets configured
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] SQL injection protection (via Prisma)
- [ ] XSS protection
- [ ] CSRF tokens implemented

### 3. Compliance Checklist

- [ ] Legal review completed
- [ ] Privacy policy published
- [ ] Terms of service published
- [ ] KYC/AML procedures documented
- [ ] Required licenses obtained (varies by jurisdiction)
- [ ] Tax reporting procedures in place

## Deployment Steps

### Option 1: Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

### Option 2: Docker Deployment

```bash
# Build Docker image
docker build -t crypto-onramp .

# Run container
docker run -p 3000:3000 \
  -e DATABASE_URL=... \
  -e STRIPE_SECRET_KEY=... \
  crypto-onramp
```

### Option 3: Manual Deployment

```bash
# Build application
npm run build

# Start production server
npm start
```

## Environment Variables

Set these in your deployment platform:

```env
# Required
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
STRIPE_SECRET_KEY=sk_live_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXTAUTH_SECRET=...
NEXTAUTH_URL=https://yourdomain.com

# Blockchain
ETHEREUM_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/...
ETHEREUM_HOT_WALLET_PRIVATE_KEY=0x...
BITCOIN_RPC_URL=...
BITCOIN_HOT_WALLET_PRIVATE_KEY=...

# Exchange Rates
COINGECKO_API_KEY=...
BINANCE_API_KEY=...

# KYC
ONFIDO_API_KEY=...
ONFIDO_WEBHOOK_SECRET=...

# AWS
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=...

# Email
SENDGRID_API_KEY=...
FROM_EMAIL=noreply@yourdomain.com

# Monitoring
SENTRY_DSN=...

# Configuration
NODE_ENV=production
USE_TESTNET=false
ENABLE_KYC=true
PLATFORM_FEE_PERCENTAGE=2.0
```

## Post-Deployment

### 1. Verify Deployment

```bash
# Check health endpoint
curl https://yourdomain.com/api/health

# Test exchange rates
curl https://yourdomain.com/api/rates/ETH?fiatCurrency=USD&amount=100

# Verify webhook endpoint
curl -X POST https://yourdomain.com/api/webhooks/stripe \
  -H "stripe-signature: test"
```

### 2. Stripe Webhook Configuration

1. Go to Stripe Dashboard > Developers > Webhooks
2. Add endpoint: `https://yourdomain.com/api/webhooks/stripe`
3. Select events:
   - payment_intent.succeeded
   - payment_intent.payment_failed
   - charge.refunded
   - charge.dispute.created
4. Copy webhook secret to environment variables

### 3. Test Transactions

**Test Mode:**
```bash
# Use test API keys
STRIPE_SECRET_KEY=sk_test_...

# Test card: 4242 4242 4242 4242
# Test blockchain: Use testnets (Goerli, Sepolia)
```

**Production:**
```bash
# Start with small amounts
# Monitor closely for first 24-48 hours
# Check transaction logs
# Verify crypto is being sent correctly
```

### 4. Monitoring Setup

**Key Metrics to Track:**
- Transaction volume
- Success rate
- Average processing time
- Failed transactions
- Crypto wallet balances
- API error rates

**Set up Alerts for:**
- Low hot wallet balance
- Failed crypto transactions
- High error rates
- Unusual transaction patterns
- Payment failures

### 5. Backup Procedures

```bash
# Database backups
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Automated daily backups
0 2 * * * pg_dump $DATABASE_URL > /backups/backup_$(date +%Y%m%d).sql
```

## Scaling Considerations

### Database
- Enable connection pooling
- Set up read replicas for analytics
- Partition large tables (transactions)

### Redis
- Use Redis Cluster for high availability
- Configure persistence for critical data

### Hot Wallet Management
- Monitor balance hourly
- Automatic refill from cold wallet
- Alert when balance < threshold

### Rate Limiting
- Per-user limits
- Per-IP limits
- Global API limits

## Maintenance

### Daily
- Check transaction processing
- Monitor error logs
- Review failed transactions
- Check wallet balances

### Weekly
- Review KYC submissions
- Analyze transaction patterns
- Update exchange rate sources
- Check security logs

### Monthly
- Security audit
- Performance review
- Compliance review
- Update dependencies

## Rollback Procedure

```bash
# Vercel
vercel rollback

# Docker
docker pull crypto-onramp:previous-tag
docker stop crypto-onramp
docker run crypto-onramp:previous-tag

# Database rollback
psma migrate reset --skip-seed
prisma migrate deploy --to <previous-migration>
```

## Support & Troubleshooting

### Common Issues

**Problem: Crypto not sending**
- Check hot wallet balance
- Verify RPC endpoint is accessible
- Check transaction logs
- Ensure private key is correct

**Problem: Payments failing**
- Verify Stripe API keys
- Check webhook configuration
- Review Stripe logs
- Test with different payment method

**Problem: High error rate**
- Check database connection
- Verify Redis is running
- Review application logs
- Check third-party API limits

### Getting Help

- Stripe Support: https://support.stripe.com
- Documentation: /docs
- Status Page: https://status.stripe.com
- Community Forum: [Your forum]

## Legal Disclaimer

This application processes financial transactions and handles cryptocurrency. Ensure you:

1. Have proper licenses for your jurisdiction
2. Comply with KYC/AML regulations
3. Maintain proper records
4. Have appropriate insurance
5. Consult with legal counsel

Failure to comply with regulations may result in fines, license revocation, or criminal charges.
