#!/bin/bash

# Database Setup Script for Stripe Crypto Onramp
# This script sets up PostgreSQL and Redis for development

set -e  # Exit on error

echo "🚀 Setting up databases for Stripe Crypto Onramp..."
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "📍 Detected OS: $MACHINE"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if Homebrew is installed (Mac only)
check_homebrew() {
    if [ "$MACHINE" = "Mac" ]; then
        if ! command -v brew &> /dev/null; then
            print_error "Homebrew not found. Please install from https://brew.sh"
            exit 1
        fi
        print_success "Homebrew found"
    fi
}

# Install PostgreSQL
install_postgresql() {
    echo ""
    echo "📦 Installing PostgreSQL..."

    if [ "$MACHINE" = "Mac" ]; then
        if command -v psql &> /dev/null; then
            print_warning "PostgreSQL already installed"
        else
            brew install postgresql@16
            brew services start postgresql@16
            print_success "PostgreSQL installed and started"
        fi
    elif [ "$MACHINE" = "Linux" ]; then
        if command -v psql &> /dev/null; then
            print_warning "PostgreSQL already installed"
        else
            sudo apt update
            sudo apt install -y postgresql postgresql-contrib
            sudo systemctl start postgresql
            sudo systemctl enable postgresql
            print_success "PostgreSQL installed and started"
        fi
    fi
}

# Install Redis
install_redis() {
    echo ""
    echo "📦 Installing Redis..."

    if [ "$MACHINE" = "Mac" ]; then
        if command -v redis-cli &> /dev/null; then
            print_warning "Redis already installed"
        else
            brew install redis
            brew services start redis
            print_success "Redis installed and started"
        fi
    elif [ "$MACHINE" = "Linux" ]; then
        if command -v redis-cli &> /dev/null; then
            print_warning "Redis already installed"
        else
            sudo apt update
            sudo apt install -y redis-server
            sudo systemctl start redis-server
            sudo systemctl enable redis-server
            print_success "Redis installed and started"
        fi
    fi
}

# Create PostgreSQL database and user
setup_postgresql_database() {
    echo ""
    echo "🗄️  Setting up PostgreSQL database..."

    DB_NAME="crypto_onramp"
    DB_USER="crypto_user"
    DB_PASSWORD="crypto_dev_password_$(openssl rand -hex 8)"

    if [ "$MACHINE" = "Mac" ]; then
        # Check if database exists
        if psql postgres -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
            print_warning "Database $DB_NAME already exists"
        else
            # Create user
            psql postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || true

            # Create database
            psql postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" 2>/dev/null || true

            # Grant privileges
            psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null || true

            print_success "Database created: $DB_NAME"
            print_success "User created: $DB_USER"
        fi
    elif [ "$MACHINE" = "Linux" ]; then
        # Check if database exists
        if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
            print_warning "Database $DB_NAME already exists"
        else
            # Create user
            sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || true

            # Create database
            sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" 2>/dev/null || true

            # Grant privileges
            sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null || true

            print_success "Database created: $DB_NAME"
            print_success "User created: $DB_USER"
        fi
    fi

    # Save connection string to .env.local
    CONNECTION_STRING="postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME"
    echo ""
    echo "📝 Database connection string:"
    echo "   $CONNECTION_STRING"
    echo ""

    # Update .env.local if it exists
    if [ -f ".env.local" ]; then
        # Check if DATABASE_URL exists and replace it
        if grep -q "^DATABASE_URL=" .env.local; then
            if [ "$MACHINE" = "Mac" ]; then
                sed -i '' "s|^DATABASE_URL=.*|DATABASE_URL=\"$CONNECTION_STRING\"|" .env.local
            else
                sed -i "s|^DATABASE_URL=.*|DATABASE_URL=\"$CONNECTION_STRING\"|" .env.local
            fi
            print_success "Updated DATABASE_URL in .env.local"
        else
            echo "DATABASE_URL=\"$CONNECTION_STRING\"" >> .env.local
            print_success "Added DATABASE_URL to .env.local"
        fi
    else
        print_warning ".env.local not found. Create it from .env.example first"
    fi
}

# Test Redis connection
test_redis() {
    echo ""
    echo "🧪 Testing Redis connection..."

    if redis-cli ping &> /dev/null; then
        print_success "Redis is running and accepting connections"

        # Update .env.local with Redis URL
        if [ -f ".env.local" ]; then
            if grep -q "^REDIS_URL=" .env.local; then
                if [ "$MACHINE" = "Mac" ]; then
                    sed -i '' 's|^REDIS_URL=.*|REDIS_URL="redis://localhost:6379"|' .env.local
                else
                    sed -i 's|^REDIS_URL=.*|REDIS_URL="redis://localhost:6379"|' .env.local
                fi
            else
                echo 'REDIS_URL="redis://localhost:6379"' >> .env.local
            fi
            print_success "Updated REDIS_URL in .env.local"
        fi
    else
        print_error "Redis is not responding"
        exit 1
    fi
}

# Test PostgreSQL connection
test_postgresql() {
    echo ""
    echo "🧪 Testing PostgreSQL connection..."

    if psql postgres -c '\q' &> /dev/null || sudo -u postgres psql -c '\q' &> /dev/null; then
        print_success "PostgreSQL is running and accepting connections"
    else
        print_error "PostgreSQL is not responding"
        exit 1
    fi
}

# Main installation flow
main() {
    check_homebrew
    install_postgresql
    install_redis
    setup_postgresql_database
    test_postgresql
    test_redis

    echo ""
    echo "======================================"
    echo "✅ Database setup complete!"
    echo "======================================"
    echo ""
    echo "Next steps:"
    echo "1. Run 'npm install' if you haven't already"
    echo "2. Run 'npx prisma migrate dev' to create database tables"
    echo "3. Run 'npm run dev' to start the application"
    echo ""
    echo "Your databases are ready:"
    echo "  PostgreSQL: localhost:5432"
    echo "  Redis: localhost:6379"
    echo ""
}

# Run main function
main
