# Redis Setup Skill

## Overview
This skill provides comprehensive guidance for setting up Redis on macOS, Linux, and Windows. Redis is an in-memory data structure store used as a database, cache, message broker, and streaming engine.

## Capabilities
- Install Redis on macOS, Linux, and Windows
- Configure Redis for caching and sessions
- Set up Redis with persistence
- Configure Redis Cluster
- Set up Redis Sentinel for high availability
- Secure Redis instances
- Monitor Redis performance
- Integrate with Node.js, Python, and other languages
- Set up Redis as a message queue
- Configure Redis for pub/sub

## Prerequisites
- Command line access
- Administrator/sudo privileges (for installation)
- Basic understanding of key-value stores

## macOS Installation

### Option 1: Homebrew (Recommended)

```bash
# Install Redis
brew install redis

# Start Redis service
brew services start redis

# Start Redis in foreground (for testing)
redis-server

# Verify installation
redis-cli ping
# Output: PONG

# Check Redis version
redis-cli --version
# Output: redis-cli 7.x.x
```

### Option 2: Docker

```bash
# Pull Redis image
docker pull redis:7-alpine

# Run Redis container
docker run --name redis-dev \
  -p 6379:6379 \
  -d redis:7-alpine

# Run with persistence
docker run --name redis-dev \
  -p 6379:6379 \
  -v redis-data:/data \
  -d redis:7-alpine redis-server --appendonly yes

# Connect to Redis
docker exec -it redis-dev redis-cli

# View logs
docker logs redis-dev
```

## Linux Installation

### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Redis
sudo apt install redis-server

# Start Redis service
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verify installation
redis-cli ping
```

### CentOS/RHEL/Fedora

```bash
# Install Redis
sudo dnf install redis

# Start Redis service
sudo systemctl start redis
sudo systemctl enable redis

# Verify installation
redis-cli ping
```

### From Source (Latest Version)

```bash
# Install dependencies
sudo apt install build-essential tcl

# Download Redis
cd /tmp
wget https://download.redis.io/redis-stable.tar.gz
tar -xzvf redis-stable.tar.gz
cd redis-stable

# Compile
make
make test

# Install
sudo make install

# Create directories
sudo mkdir /etc/redis
sudo mkdir /var/redis

# Copy configuration
sudo cp redis.conf /etc/redis/redis.conf

# Start Redis
redis-server /etc/redis/redis.conf
```

## Windows Installation

### Option 1: WSL2 (Recommended)

```bash
# Install WSL2 first
wsl --install

# Then follow Linux installation steps
```

### Option 2: Memurai (Windows Native)

1. Download from https://www.memurai.com/
2. Run installer
3. Memurai runs as a Windows service

### Option 3: Docker Desktop

```bash
# Same Docker commands as macOS
docker run --name redis-dev -p 6379:6379 -d redis:7-alpine
```

## Basic Configuration

### redis.conf

Located at:
- macOS (Homebrew): `/opt/homebrew/etc/redis.conf`
- Linux: `/etc/redis/redis.conf`
- Docker: Mount custom config

Key settings:

```conf
# Bind to localhost only (default)
bind 127.0.0.1 ::1

# Production: bind to all interfaces
bind 0.0.0.0

# Port
port 6379

# Daemonize (run in background)
daemonize yes

# Log file
logfile /var/log/redis/redis-server.log

# Database file
dir /var/lib/redis
dbfilename dump.rdb

# Maximum memory
maxmemory 256mb

# Eviction policy when max memory reached
maxmemory-policy allkeys-lru

# Password protection
requirepass your_strong_password_here

# Persistence - RDB (snapshots)
save 900 1      # After 900 sec if at least 1 key changed
save 300 10     # After 300 sec if at least 10 keys changed
save 60 10000   # After 60 sec if at least 10000 keys changed

# Persistence - AOF (append-only file)
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec  # fsync every second
```

### Apply Configuration

```bash
# Restart Redis with config
redis-server /path/to/redis.conf

# Reload config without restart (some settings)
redis-cli CONFIG REWRITE

# Check config
redis-cli CONFIG GET maxmemory
redis-cli CONFIG GET requirepass
```

## Connection Strings

### Format
```
redis://[username]:[password]@[host]:[port]/[database]
```

### Examples

```bash
# Local without password
redis://localhost:6379

# With password
redis://:your_password@localhost:6379

# Specific database (0-15)
redis://localhost:6379/0
redis://localhost:6379/1

# Remote server
redis://:password@redis.example.com:6379

# TLS/SSL
rediss://:password@redis.example.com:6380

# For Node.js ioredis
redis://user:password@localhost:6379/0?family=4
```

## Basic Commands

### Connect to Redis

```bash
# Connect to local Redis
redis-cli

# Connect to remote Redis
redis-cli -h hostname -p 6379

# With password
redis-cli -a your_password

# Select database
redis-cli -n 1

# Test connection
redis-cli ping
```

### String Operations

```bash
# Set key-value
SET key "value"
SET user:1000:name "John Doe"

# Set with expiration (seconds)
SETEX session:abc123 3600 "user_data"

# Set if not exists
SETNX lock:resource1 "locked"

# Get value
GET key

# Multiple operations
MSET key1 "value1" key2 "value2"
MGET key1 key2

# Increment/Decrement
INCR counter
INCRBY counter 5
DECR counter
DECRBY counter 5

# Append to string
APPEND key " additional text"

# Get string length
STRLEN key
```

### Hash Operations

```bash
# Set hash fields
HSET user:1000 name "John" email "john@example.com" age 30

# Set single field
HSET user:1000 city "New York"

# Get single field
HGET user:1000 name

# Get all fields
HGETALL user:1000

# Get multiple fields
HMGET user:1000 name email

# Check if field exists
HEXISTS user:1000 name

# Delete field
HDEL user:1000 age

# Increment number in hash
HINCRBY user:1000 age 1

# Get all keys
HKEYS user:1000

# Get all values
HVALS user:1000
```

### List Operations

```bash
# Push to list
LPUSH mylist "item1"  # Left push
RPUSH mylist "item2"  # Right push

# Push multiple
LPUSH mylist "item1" "item2" "item3"

# Pop from list
LPOP mylist  # Left pop
RPOP mylist  # Right pop

# Get list range
LRANGE mylist 0 -1  # All items
LRANGE mylist 0 9   # First 10 items

# List length
LLEN mylist

# Get by index
LINDEX mylist 0

# Set by index
LSET mylist 0 "new value"

# Trim list
LTRIM mylist 0 99  # Keep first 100 items
```

### Set Operations

```bash
# Add members to set
SADD tags "redis" "database" "cache"

# Remove member
SREM tags "cache"

# Check membership
SISMEMBER tags "redis"

# Get all members
SMEMBERS tags

# Set size
SCARD tags

# Random member
SRANDMEMBER tags

# Pop random member
SPOP tags

# Set operations
SUNION set1 set2      # Union
SINTER set1 set2      # Intersection
SDIFF set1 set2       # Difference
```

### Sorted Set Operations

```bash
# Add members with scores
ZADD leaderboard 100 "player1" 200 "player2" 150 "player3"

# Get rank (0-based)
ZRANK leaderboard "player1"

# Get score
ZSCORE leaderboard "player1"

# Increment score
ZINCRBY leaderboard 10 "player1"

# Range by rank
ZRANGE leaderboard 0 -1              # All, ascending
ZREVRANGE leaderboard 0 9            # Top 10, descending

# Range by score
ZRANGEBYSCORE leaderboard 100 200

# Count by score range
ZCOUNT leaderboard 100 200

# Remove member
ZREM leaderboard "player1"
```

### Expiration and TTL

```bash
# Set expiration (seconds)
EXPIRE key 3600

# Set expiration at timestamp
EXPIREAT key 1735689600

# Set expiration (milliseconds)
PEXPIRE key 60000

# Check TTL
TTL key          # Returns seconds
PTTL key         # Returns milliseconds

# Remove expiration
PERSIST key
```

### Key Management

```bash
# List all keys (dangerous in production)
KEYS *

# Better: scan keys
SCAN 0 MATCH user:* COUNT 100

# Check if key exists
EXISTS key

# Delete key
DEL key

# Delete multiple keys
DEL key1 key2 key3

# Rename key
RENAME oldkey newkey

# Get key type
TYPE key

# Get random key
RANDOMKEY
```

## Caching Patterns

### Cache-Aside (Lazy Loading)

```javascript
// Node.js example with ioredis
const Redis = require('ioredis');
const redis = new Redis();

async function getUser(userId) {
  const cacheKey = `user:${userId}`;

  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Cache miss - get from database
  const user = await database.getUser(userId);

  // Store in cache (1 hour TTL)
  await redis.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}
```

### Write-Through Cache

```javascript
async function updateUser(userId, data) {
  // Update database
  await database.updateUser(userId, data);

  // Update cache
  const cacheKey = `user:${userId}`;
  await redis.setex(cacheKey, 3600, JSON.stringify(data));
}
```

### Cache Warming

```javascript
async function warmCache() {
  const users = await database.getPopularUsers();

  for (const user of users) {
    const cacheKey = `user:${user.id}`;
    await redis.setex(cacheKey, 3600, JSON.stringify(user));
  }
}
```

## Session Management

```javascript
// Store session
async function createSession(sessionId, userData) {
  await redis.setex(
    `session:${sessionId}`,
    86400, // 24 hours
    JSON.stringify(userData)
  );
}

// Get session
async function getSession(sessionId) {
  const data = await redis.get(`session:${sessionId}`);
  return data ? JSON.parse(data) : null;
}

// Extend session
async function touchSession(sessionId) {
  await redis.expire(`session:${sessionId}`, 86400);
}

// Destroy session
async function destroySession(sessionId) {
  await redis.del(`session:${sessionId}`);
}
```

## Pub/Sub

### Publisher

```javascript
const Redis = require('ioredis');
const publisher = new Redis();

// Publish message
publisher.publish('notifications', JSON.stringify({
  type: 'new_order',
  orderId: '12345'
}));
```

### Subscriber

```javascript
const Redis = require('ioredis');
const subscriber = new Redis();

// Subscribe to channel
subscriber.subscribe('notifications', (err, count) => {
  console.log(`Subscribed to ${count} channel(s)`);
});

// Handle messages
subscriber.on('message', (channel, message) => {
  console.log(`Received from ${channel}:`, message);
  const data = JSON.parse(message);
  // Process message
});

// Pattern subscribe
subscriber.psubscribe('notification:*', (err, count) => {
  console.log(`Subscribed to ${count} pattern(s)`);
});
```

## Rate Limiting

### Fixed Window

```javascript
async function rateLimitFixed(userId, limit = 100, window = 60) {
  const key = `ratelimit:${userId}:${Math.floor(Date.now() / (window * 1000))}`;

  const count = await redis.incr(key);

  if (count === 1) {
    await redis.expire(key, window);
  }

  return count <= limit;
}
```

### Sliding Window

```javascript
async function rateLimitSliding(userId, limit = 100, window = 60) {
  const key = `ratelimit:${userId}`;
  const now = Date.now();
  const windowStart = now - (window * 1000);

  // Remove old entries
  await redis.zremrangebyscore(key, 0, windowStart);

  // Count entries in window
  const count = await redis.zcard(key);

  if (count < limit) {
    // Add new entry
    await redis.zadd(key, now, `${now}-${Math.random()}`);
    await redis.expire(key, window);
    return true;
  }

  return false;
}
```

## Persistence

### RDB (Snapshot)

```conf
# redis.conf
save 900 1       # After 15 min if 1 key changed
save 300 10      # After 5 min if 10 keys changed
save 60 10000    # After 1 min if 10000 keys changed

# Trigger manual save
redis-cli BGSAVE

# Synchronous save (blocks)
redis-cli SAVE
```

### AOF (Append-Only File)

```conf
# redis.conf
appendonly yes
appendfilename "appendonly.aof"

# Sync strategy
appendfsync always    # Slowest, safest
appendfsync everysec  # Good balance (default)
appendfsync no        # Fastest, least safe

# Rewrite AOF when it grows too large
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

Manually rewrite AOF:
```bash
redis-cli BGREWRITEAOF
```

## Security

### 1. Password Protection

```conf
# redis.conf
requirepass your_strong_password_here

# ACL (Redis 6+)
user default on >password ~* &* +@all
user readonly on >readonlypass ~* &* +@read
```

### 2. Disable Dangerous Commands

```conf
# redis.conf
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command CONFIG "CONFIG-aB3xY9mN"
rename-command SHUTDOWN "SHUTDOWN-pQ7Rz2Wk"
```

### 3. Network Security

```conf
# Bind to specific IPs
bind 127.0.0.1 192.168.1.100

# Enable protected mode
protected-mode yes

# Disable external access
bind 127.0.0.1 ::1
```

### 4. TLS/SSL

```conf
# Generate certificates
tls-port 6380
tls-cert-file /path/to/redis.crt
tls-key-file /path/to/redis.key
tls-ca-cert-file /path/to/ca.crt

# Require TLS for all connections
tls-auth-clients yes
```

### 5. Firewall

```bash
# Ubuntu/Debian
sudo ufw allow from 192.168.1.0/24 to any port 6379
sudo ufw deny 6379

# iptables
sudo iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 6379 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 6379 -j DROP
```

## Monitoring

### INFO Command

```bash
# All info
redis-cli INFO

# Specific sections
redis-cli INFO server
redis-cli INFO clients
redis-cli INFO memory
redis-cli INFO persistence
redis-cli INFO stats
redis-cli INFO replication
redis-cli INFO cpu
redis-cli INFO keyspace
```

### Monitor Real-time

```bash
# Monitor all commands
redis-cli MONITOR

# Get slowlog
redis-cli SLOWLOG GET 10

# Configure slowlog
redis-cli CONFIG SET slowlog-log-slower-than 10000  # 10ms
redis-cli CONFIG SET slowlog-max-len 128
```

### Memory Usage

```bash
# Total memory
redis-cli INFO memory | grep used_memory_human

# Memory by key
redis-cli --bigkeys

# Memory analysis
redis-cli --memkeys

# Memory usage of specific key
redis-cli MEMORY USAGE keyname
```

## Redis Client Libraries

### Node.js (ioredis)

```javascript
const Redis = require('ioredis');

// Basic connection
const redis = new Redis();

// With options
const redis = new Redis({
  host: 'localhost',
  port: 6379,
  password: 'auth',
  db: 0,
  retryStrategy: (times) => Math.min(times * 50, 2000)
});

// Cluster
const cluster = new Redis.Cluster([
  { host: 'localhost', port: 7000 },
  { host: 'localhost', port: 7001 },
]);

// Usage
await redis.set('key', 'value');
const value = await redis.get('key');
```

### Python (redis-py)

```python
import redis

# Basic connection
r = redis.Redis(host='localhost', port=6379, db=0)

# With password
r = redis.Redis(
    host='localhost',
    port=6379,
    password='your_password',
    decode_responses=True
)

# Connection pool
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

# Usage
r.set('key', 'value')
value = r.get('key')
```

## Production Deployment

### Managed Services

**AWS ElastiCache for Redis**
- Automatic failover
- Automatic backups
- Multi-AZ deployment

**Google Cloud Memorystore**
- High availability
- Automatic patching

**Azure Cache for Redis**
- Built-in monitoring
- Geo-replication

**Redis Enterprise Cloud**
- Official Redis offering
- Active-active geo-distribution

**DigitalOcean Managed Redis**
- Easy setup
- Automatic backups

### Self-Hosted High Availability

#### Redis Sentinel

```bash
# sentinel.conf
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel auth-pass mymaster your_password
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 10000

# Start sentinel
redis-sentinel /path/to/sentinel.conf
```

#### Redis Cluster

```bash
# Create cluster with 3 masters and 3 replicas
redis-cli --cluster create \
  127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
  127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 \
  --cluster-replicas 1
```

## Troubleshooting

### Can't Connect

```bash
# Check if Redis is running
brew services list  # macOS
sudo systemctl status redis  # Linux
redis-cli ping

# Check port
lsof -i :6379
netstat -an | grep 6379

# Check logs
tail -f /opt/homebrew/var/log/redis.log  # macOS
tail -f /var/log/redis/redis-server.log  # Linux
```

### Memory Issues

```bash
# Check memory usage
redis-cli INFO memory

# Find large keys
redis-cli --bigkeys

# Set max memory
redis-cli CONFIG SET maxmemory 256mb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### Performance Issues

```bash
# Check slow queries
redis-cli SLOWLOG GET 10

# Monitor commands
redis-cli MONITOR

# Check latency
redis-cli --latency
redis-cli --latency-history

# Benchmark
redis-benchmark -q -n 100000
```

## Quick Reference

```bash
# Start/Stop
brew services start redis
brew services stop redis
brew services restart redis

# Connect
redis-cli
redis-cli -h hostname -p 6379 -a password

# Basic operations
SET key value
GET key
DEL key
EXISTS key
KEYS pattern
EXPIRE key seconds

# Info
INFO
INFO memory
MONITOR
SLOWLOG GET 10
```

## Resources

- [Official Documentation](https://redis.io/documentation)
- [Redis Commands](https://redis.io/commands)
- [Redis University](https://university.redis.com/)
- [Redis Labs Blog](https://redis.com/blog/)
- [Try Redis](https://try.redis.io/)

## Support

For help:
- Redis Discord
- Stack Overflow
- Redis mailing list
- #redis on Freenode IRC
