# Database Setup Guide for Stripe Crypto Onramp

This guide will help you set up PostgreSQL and Redis for the Stripe Crypto Onramp application.

## Quick Setup (Automated)

### Run the Setup Script

```bash
cd /Users/bastiendumont/Documents/GitHub/ByteClaude/examples/stripe-crypto-onramp
./scripts/setup-databases.sh
```

This script will:
- ✅ Install PostgreSQL
- ✅ Install Redis
- ✅ Create database and user
- ✅ Start both services
- ✅ Update your `.env.local` file
- ✅ Test connections

After running the script, skip to [Next Steps](#next-steps).

---

## Manual Setup

If you prefer to set up manually or the script doesn't work for your system:

### 1. Install PostgreSQL

#### macOS (Homebrew)

```bash
# Install PostgreSQL
brew install postgresql@16

# Start PostgreSQL service
brew services start postgresql@16

# Verify installation
psql --version
```

#### macOS (Postgres.app)

1. Download from https://postgresapp.com/
2. Move to Applications
3. Open and click "Initialize"

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Docker

```bash
docker run --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_DB=crypto_onramp \
  -p 5432:5432 \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres:16
```

### 2. Install Redis

#### macOS (Homebrew)

```bash
# Install Redis
brew install redis

# Start Redis service
brew services start redis

# Verify installation
redis-cli ping
# Should output: PONG
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### Docker

```bash
docker run --name redis-dev \
  -p 6379:6379 \
  -d redis:7-alpine
```

### 3. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql postgres

# Create user
CREATE USER crypto_user WITH PASSWORD 'your_secure_password';

# Create database
CREATE DATABASE crypto_onramp OWNER crypto_user;

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE crypto_onramp TO crypto_user;

# For PostgreSQL 15+, also grant schema privileges
\c crypto_onramp
GRANT ALL ON SCHEMA public TO crypto_user;

# Exit
\q
```

### 4. Configure Environment Variables

Create or update `.env.local`:

```bash
cp .env.example .env.local
```

Add these lines to `.env.local`:

```env
# PostgreSQL
DATABASE_URL="postgresql://crypto_user:your_secure_password@localhost:5432/crypto_onramp"

# Redis
REDIS_URL="redis://localhost:6379"
```

### 5. Test Connections

#### Test PostgreSQL

```bash
# Test connection
psql "postgresql://crypto_user:your_secure_password@localhost:5432/crypto_onramp"

# Should connect successfully
# Type \q to quit
```

#### Test Redis

```bash
# Test connection
redis-cli ping

# Should output: PONG
```

## Next Steps

After setting up the databases:

### 1. Install Dependencies

```bash
npm install
```

### 2. Run Database Migrations

This will create all the tables defined in `database/schema.prisma`:

```bash
npx prisma generate
npx prisma migrate dev --name init
```

You should see output like:
```
✔ Generated Prisma Client
✔ Applied migration 20240101000000_init

Your database is now in sync with your schema.
```

### 3. (Optional) Seed Database

```bash
npm run db:seed
```

### 4. Open Prisma Studio

View and edit your database with a GUI:

```bash
npx prisma studio
```

Opens at http://localhost:5555

### 5. Start Development Server

```bash
npm run dev
```

The app will be running at http://localhost:3000

## Verify Setup

### Check PostgreSQL Tables

```bash
psql "postgresql://crypto_user:your_password@localhost:5432/crypto_onramp"
```

```sql
-- List all tables
\dt

-- You should see:
-- User
-- Transaction
-- KYCVerification
-- Wallet
-- ExchangeRate
-- etc.

-- Check a table structure
\d "Transaction"

-- Quit
\q
```

### Check Redis

```bash
redis-cli

# Test basic operations
> SET test "Hello Redis"
> GET test
> DEL test
> QUIT
```

## Troubleshooting

### PostgreSQL Won't Start

```bash
# Check if it's running
brew services list  # macOS
sudo systemctl status postgresql  # Linux

# Check port 5432
lsof -i :5432

# View logs
tail -f /opt/homebrew/var/log/postgresql@16.log  # macOS
tail -f /var/log/postgresql/postgresql-16-main.log  # Linux
```

### Can't Connect to PostgreSQL

```bash
# Make sure service is running
brew services start postgresql@16  # macOS
sudo systemctl start postgresql  # Linux

# Try connecting as postgres user
psql postgres

# If that works, your user/password might be wrong
```

### Redis Won't Start

```bash
# Check if it's running
brew services list  # macOS
sudo systemctl status redis-server  # Linux

# Check port 6379
lsof -i :6379

# View logs
tail -f /opt/homebrew/var/log/redis.log  # macOS
tail -f /var/log/redis/redis-server.log  # Linux
```

### Prisma Migration Fails

```bash
# Reset database (WARNING: deletes all data)
npx prisma migrate reset

# Then run migration again
npx prisma migrate dev --name init
```

### Permission Errors (PostgreSQL)

```sql
-- Connect to database
\c crypto_onramp

-- Grant all privileges
GRANT ALL ON SCHEMA public TO crypto_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO crypto_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO crypto_user;

-- Or make user superuser (development only!)
ALTER USER crypto_user WITH SUPERUSER;
```

## Database Management

### Backup PostgreSQL

```bash
# Backup database
pg_dump crypto_onramp > backup.sql

# Backup with compression
pg_dump crypto_onramp | gzip > backup.sql.gz

# Restore
psql crypto_onramp < backup.sql
```

### Monitor Redis

```bash
# Real-time monitoring
redis-cli MONITOR

# Get info
redis-cli INFO

# Check memory usage
redis-cli INFO memory
```

### Stop Services

```bash
# PostgreSQL
brew services stop postgresql@16  # macOS
sudo systemctl stop postgresql  # Linux

# Redis
brew services stop redis  # macOS
sudo systemctl stop redis-server  # Linux
```

## Production Considerations

For production, consider using managed database services:

### PostgreSQL Options:
- **Supabase** - Free tier available, includes Auth + Storage
- **AWS RDS** - Managed PostgreSQL
- **Google Cloud SQL** - Managed databases
- **DigitalOcean** - Managed databases
- **Railway** - Simple deployment
- **Neon** - Serverless PostgreSQL

### Redis Options:
- **Upstash** - Serverless Redis with free tier
- **Redis Cloud** - Official Redis offering
- **AWS ElastiCache** - Managed Redis
- **DigitalOcean** - Managed Redis
- **Railway** - Simple deployment

## Connection String Examples

### PostgreSQL

```env
# Local development
DATABASE_URL="postgresql://crypto_user:password@localhost:5432/crypto_onramp"

# Supabase
DATABASE_URL="postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres"

# Railway
DATABASE_URL="postgresql://postgres:[password]@containers-us-west-1.railway.app:5432/railway"

# With connection pooling
DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=5&pool_timeout=10"
```

### Redis

```env
# Local development
REDIS_URL="redis://localhost:6379"

# Upstash
REDIS_URL="redis://default:[password]@[endpoint]:6379"

# Railway
REDIS_URL="redis://default:[password]@containers-us-west-1.railway.app:6379"

# With password
REDIS_URL="redis://:password@localhost:6379"
```

## Need Help?

- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Redis Documentation: https://redis.io/documentation
- Prisma Documentation: https://www.prisma.io/docs/
- Check the skills: `/skills/postgresql/SKILL.md` and `/skills/redis/SKILL.md`
