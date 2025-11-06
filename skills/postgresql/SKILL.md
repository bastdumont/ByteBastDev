# PostgreSQL Database Setup Skill

## Overview
This skill provides comprehensive guidance for setting up PostgreSQL databases on macOS, Linux, and Windows. It covers installation, configuration, user management, database creation, and best practices for development and production environments.

## Capabilities
- Install PostgreSQL on macOS, Linux, and Windows
- Configure PostgreSQL for local development
- Create databases and users
- Set up connection strings
- Configure for production use
- Backup and restore databases
- Performance tuning
- Security hardening
- Monitor database health
- Integrate with popular ORMs (Prisma, TypeORM, Sequelize)

## Prerequisites
- Command line access
- Administrator/sudo privileges (for installation)
- Basic understanding of databases

## macOS Installation

### Option 1: Homebrew (Recommended)

```bash
# Install PostgreSQL
brew install postgresql@16

# Start PostgreSQL service
brew services start postgresql@16

# Add to PATH
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
psql --version
# Output: psql (PostgreSQL) 16.x
```

### Option 2: Postgres.app

1. Download from https://postgresapp.com/
2. Move to Applications folder
3. Open Postgres.app
4. Click "Initialize" to create a new server
5. Add to PATH:
```bash
echo 'export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Option 3: Docker

```bash
# Pull PostgreSQL image
docker pull postgres:16

# Run PostgreSQL container
docker run --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=myapp \
  -p 5432:5432 \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres:16

# Connect to PostgreSQL
docker exec -it postgres-dev psql -U postgres
```

## Linux Installation

### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify installation
psql --version
```

### CentOS/RHEL/Fedora

```bash
# Install PostgreSQL
sudo dnf install postgresql-server postgresql-contrib

# Initialize database
sudo postgresql-setup --initdb

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Windows Installation

### Option 1: Installer

1. Download from https://www.postgresql.org/download/windows/
2. Run the installer
3. Follow the setup wizard
4. Remember the password you set for the postgres user
5. PostgreSQL runs as a Windows service automatically

### Option 2: Docker Desktop

```bash
# Same Docker command as macOS above
docker run --name postgres-dev -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres:16
```

## Initial Configuration

### Connect to PostgreSQL

```bash
# Connect as postgres user (macOS/Linux)
psql postgres

# On Linux, you might need to switch user first
sudo -u postgres psql

# On Windows (using PowerShell)
psql -U postgres
```

### Create a New User

```sql
-- Create user with password
CREATE USER myapp_user WITH PASSWORD 'secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE myapp TO myapp_user;

-- For PostgreSQL 15+, grant schema privileges
\c myapp
GRANT ALL ON SCHEMA public TO myapp_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myapp_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO myapp_user;

-- Make user a superuser (development only)
ALTER USER myapp_user WITH SUPERUSER;
```

### Create a Database

```sql
-- Create database
CREATE DATABASE myapp;

-- Create database with owner
CREATE DATABASE myapp OWNER myapp_user;

-- Create database with encoding
CREATE DATABASE myapp
  WITH OWNER = myapp_user
  ENCODING = 'UTF8'
  LC_COLLATE = 'en_US.UTF-8'
  LC_CTYPE = 'en_US.UTF-8'
  TEMPLATE = template0;

-- List all databases
\l

-- Connect to database
\c myapp

-- List all tables
\dt

-- Quit psql
\q
```

## Connection Strings

### Format
```
postgresql://[user]:[password]@[host]:[port]/[database]?[parameters]
```

### Examples

```bash
# Local development
DATABASE_URL="postgresql://postgres:password@localhost:5432/myapp"

# With custom user
DATABASE_URL="postgresql://myapp_user:secure_password@localhost:5432/myapp"

# Remote server
DATABASE_URL="postgresql://user:pass@db.example.com:5432/production_db"

# With SSL
DATABASE_URL="postgresql://user:pass@db.example.com:5432/mydb?sslmode=require"

# Connection pooling (for Prisma)
DATABASE_URL="postgresql://user:pass@localhost:5432/mydb?connection_limit=5"

# Multiple parameters
DATABASE_URL="postgresql://user:pass@localhost:5432/mydb?sslmode=require&connect_timeout=10&application_name=myapp"
```

### SSL Modes
- `disable` - No SSL
- `allow` - Try SSL, fallback to non-SSL
- `prefer` - Try SSL, fallback to non-SSL (default)
- `require` - Require SSL
- `verify-ca` - Require SSL and verify certificate
- `verify-full` - Require SSL and verify certificate and hostname

## Configuration Files

### postgresql.conf

Located at:
- macOS (Homebrew): `/opt/homebrew/var/postgresql@16/postgresql.conf`
- Linux: `/etc/postgresql/16/main/postgresql.conf`
- Windows: `C:\Program Files\PostgreSQL\16\data\postgresql.conf`

Key settings:
```conf
# Connection Settings
listen_addresses = 'localhost'  # Production: '*' or specific IP
port = 5432
max_connections = 100

# Memory Settings
shared_buffers = 256MB          # 25% of RAM for dedicated server
effective_cache_size = 1GB      # 50-75% of RAM
work_mem = 4MB                  # RAM / max_connections / 2
maintenance_work_mem = 64MB

# Write-Ahead Log
wal_buffers = 16MB
checkpoint_completion_target = 0.9

# Query Tuning
random_page_cost = 1.1          # For SSD
effective_io_concurrency = 200  # For SSD

# Logging
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d.log'
log_statement = 'all'           # Development only
log_duration = on
log_min_duration_statement = 1000  # Log queries > 1 second
```

### pg_hba.conf

Authentication configuration:
```conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# Local connections
local   all             all                                     trust
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5

# Remote connections (production)
host    all             all             0.0.0.0/0               md5
host    all             all             ::/0                    md5
```

Reload configuration:
```bash
# Method 1: SQL
SELECT pg_reload_conf();

# Method 2: Command line
pg_ctl reload

# Method 3: Service restart
sudo systemctl restart postgresql
```

## Database Management

### Backup Database

```bash
# Backup single database
pg_dump myapp > myapp_backup.sql

# Backup with compression
pg_dump myapp | gzip > myapp_backup.sql.gz

# Backup specific user
pg_dump -U myapp_user myapp > backup.sql

# Backup all databases
pg_dumpall > all_databases_backup.sql

# Custom format (recommended for large databases)
pg_dump -Fc myapp > myapp_backup.dump
```

### Restore Database

```bash
# Restore from SQL
psql myapp < myapp_backup.sql

# Restore from compressed
gunzip < myapp_backup.sql.gz | psql myapp

# Restore custom format
pg_restore -d myapp myapp_backup.dump

# Restore with clean (drop existing objects)
pg_restore -d myapp -c myapp_backup.dump
```

### Database Size

```sql
-- Database size
SELECT pg_size_pretty(pg_database_size('myapp'));

-- Table sizes
SELECT
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Total database size
SELECT
  datname,
  pg_size_pretty(pg_database_size(datname)) AS size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;
```

## Performance Tuning

### Indexes

```sql
-- Create index
CREATE INDEX idx_users_email ON users(email);

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Partial index
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Multi-column index
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- List indexes
\di

-- Index size
SELECT
  indexrelname AS index_name,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;

-- Unused indexes
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Query Optimization

```sql
-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Vacuum database (reclaim space)
VACUUM ANALYZE;

-- Full vacuum (locks table)
VACUUM FULL;

-- Analyze tables (update statistics)
ANALYZE;

-- Reindex database
REINDEX DATABASE myapp;
```

### Connection Pooling

Use PgBouncer for connection pooling:

```bash
# Install PgBouncer
brew install pgbouncer  # macOS
sudo apt install pgbouncer  # Linux

# Configure /etc/pgbouncer/pgbouncer.ini
[databases]
myapp = host=localhost port=5432 dbname=myapp

[pgbouncer]
listen_addr = 127.0.0.1
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20

# Start PgBouncer
pgbouncer -d /etc/pgbouncer/pgbouncer.ini

# Connect through PgBouncer
psql -h localhost -p 6432 -U myapp_user myapp
```

## Security Best Practices

### 1. Strong Passwords

```sql
-- Create user with strong password
CREATE USER myapp WITH PASSWORD 'aB3$xY9!mN2#pQ7@';

-- Change password
ALTER USER myapp WITH PASSWORD 'new_secure_password';
```

### 2. Limit User Permissions

```sql
-- Create read-only user
CREATE USER readonly WITH PASSWORD 'password';
GRANT CONNECT ON DATABASE myapp TO readonly;
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly;
```

### 3. SSL/TLS Encryption

```bash
# Generate SSL certificates
openssl req -new -x509 -days 365 -nodes -text \
  -out server.crt \
  -keyout server.key \
  -subj "/CN=localhost"

# Set permissions
chmod 600 server.key

# Update postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
```

### 4. Firewall Rules

```bash
# Ubuntu/Debian - allow only localhost
sudo ufw allow from 127.0.0.1 to any port 5432

# Allow specific IP
sudo ufw allow from 192.168.1.100 to any port 5432
```

## Monitoring

### Active Connections

```sql
-- Current connections
SELECT * FROM pg_stat_activity;

-- Kill query
SELECT pg_cancel_backend(pid);

-- Kill connection
SELECT pg_terminate_backend(pid);

-- Connection count by database
SELECT
  datname,
  count(*) as connections
FROM pg_stat_activity
GROUP BY datname;
```

### Slow Queries

```sql
-- Install pg_stat_statements extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- View slow queries
SELECT
  query,
  calls,
  total_exec_time,
  mean_exec_time,
  max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

## ORM Integration

### Prisma

```bash
# Install Prisma
npm install prisma --save-dev
npm install @prisma/client

# Initialize Prisma
npx prisma init

# Create schema (prisma/schema.prisma)
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

# Generate Prisma Client
npx prisma generate

# Create migration
npx prisma migrate dev --name init

# Push schema without migration
npx prisma db push

# Open Prisma Studio
npx prisma studio
```

### TypeORM

```typescript
import { DataSource } from 'typeorm';

const AppDataSource = new DataSource({
  type: 'postgres',
  host: 'localhost',
  port: 5432,
  username: 'myapp_user',
  password: 'password',
  database: 'myapp',
  entities: ['src/entities/**/*.ts'],
  synchronize: true, // Don't use in production
  logging: true,
});
```

## Troubleshooting

### Can't Connect

```bash
# Check if PostgreSQL is running
brew services list  # macOS
sudo systemctl status postgresql  # Linux

# Check port
lsof -i :5432
netstat -an | grep 5432

# Check logs
tail -f /opt/homebrew/var/log/postgresql@16.log  # macOS
tail -f /var/log/postgresql/postgresql-16-main.log  # Linux
```

### Permission Denied

```sql
-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE myapp TO myapp_user;
GRANT ALL ON SCHEMA public TO myapp_user;
ALTER USER myapp_user WITH SUPERUSER;
```

### Out of Disk Space

```bash
# Check database size
du -sh /opt/homebrew/var/postgresql@16

# Vacuum to reclaim space
psql -d myapp -c "VACUUM FULL;"

# Clean old WAL files
pg_archivecleanup /path/to/archive 000000010000000000000010
```

## Production Deployment

### Managed Services

**AWS RDS for PostgreSQL**
- Automatic backups
- Multi-AZ deployment
- Read replicas
- Monitoring with CloudWatch

**Google Cloud SQL**
- High availability
- Automatic storage increase
- Built-in backups

**Azure Database for PostgreSQL**
- Flexible server
- Built-in security
- Automatic patching

**DigitalOcean Managed Databases**
- Easy setup
- Automatic backups
- Connection pooling included

**Supabase**
- PostgreSQL with REST API
- Real-time subscriptions
- Built-in authentication

### Self-Hosted

```bash
# Production checklist
- [ ] Use strong passwords
- [ ] Enable SSL/TLS
- [ ] Configure firewall
- [ ] Set up automated backups
- [ ] Configure replication
- [ ] Set up monitoring
- [ ] Regular security updates
- [ ] Connection pooling (PgBouncer)
- [ ] Proper resource allocation
- [ ] Disaster recovery plan
```

## Quick Reference

### Common Commands

```bash
# Start/Stop/Restart
brew services start postgresql@16
brew services stop postgresql@16
brew services restart postgresql@16

# Connect
psql postgres
psql -U username -d database

# Dump/Restore
pg_dump myapp > backup.sql
psql myapp < backup.sql

# User management
createuser username
dropuser username

# Database management
createdb myapp
dropdb myapp
```

### psql Commands

```
\l          - List databases
\c dbname   - Connect to database
\dt         - List tables
\d table    - Describe table
\du         - List users
\dp         - List privileges
\di         - List indexes
\df         - List functions
\q          - Quit
\?          - Help
\h SQL      - SQL command help
```

## Resources

- [Official Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [PgExercises](https://pgexercises.com/) - Practice SQL
- [PostgreSQL Wiki](https://wiki.postgresql.org/)
- [Awesome PostgreSQL](https://github.com/dhamaniasad/awesome-postgres)

## Support

For help:
- PostgreSQL mailing lists
- Stack Overflow
- PostgreSQL Slack channel
- #postgresql on Freenode IRC
