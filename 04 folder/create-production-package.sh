#!/bin/bash

# Production Deployment Package Script
# This script prepares the unified platform for production deployment

# Set environment variables
export NODE_ENV=production
export PRODUCTION_BUILD=true

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Log function
log() {
  echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
  echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

warn() {
  echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Check if required tools are installed
check_requirements() {
  log "Checking requirements..."
  
  # Check Node.js
  if ! command -v node &> /dev/null; then
    error "Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
  fi
  
  # Check npm
  if ! command -v npm &> /dev/null; then
    error "npm is not installed. Please install npm."
    exit 1
  fi
  
  # Check Docker
  if ! command -v docker &> /dev/null; then
    warn "Docker is not installed. Docker is recommended for containerized deployment."
  fi
  
  # Check Docker Compose
  if ! command -v docker-compose &> /dev/null; then
    warn "Docker Compose is not installed. Docker Compose is recommended for multi-container deployment."
  fi
  
  log "Requirements check completed."
}

# Clean build directories
clean_build() {
  log "Cleaning build directories..."
  
  # Remove previous build artifacts
  rm -rf ./dist
  rm -rf ./build
  rm -rf ./node_modules
  
  log "Build directories cleaned."
}

# Install dependencies
install_dependencies() {
  log "Installing production dependencies..."
  
  # Install dependencies
  npm ci --production
  
  if [ $? -ne 0 ]; then
    error "Failed to install dependencies."
    exit 1
  fi
  
  log "Dependencies installed successfully."
}

# Build frontend
build_frontend() {
  log "Building frontend..."
  
  # Navigate to frontend directory
  cd ./private/src/frontend
  
  # Install frontend dependencies
  npm ci
  
  # Build frontend
  npm run build
  
  if [ $? -ne 0 ]; then
    error "Failed to build frontend."
    exit 1
  fi
  
  # Move build artifacts to dist directory
  mkdir -p ../../../dist/public
  cp -r ./build/* ../../../dist/public/
  
  # Return to root directory
  cd ../../../
  
  log "Frontend built successfully."
}

# Build backend
build_backend() {
  log "Building backend..."
  
  # Navigate to backend directory
  cd ./private/src/backend
  
  # Install backend dependencies
  npm ci
  
  # Build backend
  npm run build
  
  if [ $? -ne 0 ]; then
    error "Failed to build backend."
    exit 1
  fi
  
  # Move build artifacts to dist directory
  mkdir -p ../../../dist/server
  cp -r ./dist/* ../../../dist/server/
  
  # Return to root directory
  cd ../../../
  
  log "Backend built successfully."
}

# Build AI services
build_ai_services() {
  log "Building AI services..."
  
  # Navigate to AI services directory
  cd ./private/src/ai
  
  # Install AI services dependencies
  npm ci
  
  # Build AI services
  npm run build
  
  if [ $? -ne 0 ]; then
    error "Failed to build AI services."
    exit 1
  fi
  
  # Move build artifacts to dist directory
  mkdir -p ../../../dist/ai
  cp -r ./dist/* ../../../dist/ai/
  
  # Return to root directory
  cd ../../../
  
  log "AI services built successfully."
}

# Prepare configuration files
prepare_config() {
  log "Preparing configuration files..."
  
  # Create config directory
  mkdir -p ./dist/config
  
  # Generate production configuration
  cat > ./dist/config/production.json << EOF
{
  "server": {
    "port": 3000,
    "host": "0.0.0.0",
    "cors": {
      "origin": ["https://unifiedplatform.com"],
      "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
      "allowedHeaders": ["Content-Type", "Authorization"]
    }
  },
  "database": {
    "host": "\${DB_HOST}",
    "port": "\${DB_PORT}",
    "username": "\${DB_USERNAME}",
    "password": "\${DB_PASSWORD}",
    "database": "\${DB_NAME}",
    "ssl": true
  },
  "auth": {
    "jwtSecret": "\${JWT_SECRET}",
    "jwtExpiry": "1d",
    "refreshTokenExpiry": "7d",
    "bcryptRounds": 12
  },
  "ai": {
    "serviceUrl": "http://ai-service:3001",
    "apiKey": "\${AI_API_KEY}"
  },
  "features": {
    "ageRestrictions": true,
    "kycVerification": true,
    "contentModeration": true,
    "digitalAssets": true
  },
  "logging": {
    "level": "info",
    "format": "json"
  },
  "monitoring": {
    "enabled": true,
    "interval": 15
  }
}
EOF
  
  # Create environment variables template
  cat > ./dist/.env.template << EOF
# Database Configuration
DB_HOST=production-db.unifiedplatform.com
DB_PORT=5432
DB_USERNAME=dbuser
DB_PASSWORD=
DB_NAME=unified_platform

# Authentication
JWT_SECRET=

# AI Services
AI_API_KEY=

# Monitoring
SENTRY_DSN=

# Email
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
EMAIL_FROM=noreply@unifiedplatform.com

# Storage
S3_BUCKET=
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_REGION=us-east-1
EOF
  
  log "Configuration files prepared."
}

# Prepare database migration scripts
prepare_migrations() {
  log "Preparing database migration scripts..."
  
  # Create migrations directory
  mkdir -p ./dist/migrations
  
  # Copy migration scripts
  cp -r ./private/src/backend/migrations/* ./dist/migrations/
  
  # Create migration runner script
  cat > ./dist/migrations/run-migrations.js << EOF
const { execSync } = require('child_process');
const path = require('path');

console.log('Running database migrations...');

try {
  execSync('npx sequelize-cli db:migrate', {
    env: process.env,
    stdio: 'inherit',
    cwd: path.resolve(__dirname)
  });
  console.log('Migrations completed successfully.');
} catch (error) {
  console.error('Migration failed:', error);
  process.exit(1);
}
EOF
  
  log "Migration scripts prepared."
}

# Create Docker configuration
create_docker_config() {
  log "Creating Docker configuration..."
  
  # Create Dockerfile
  cat > ./dist/Dockerfile << EOF
FROM node:16-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --production

# Copy application files
COPY . .

# Expose port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production

# Start application
CMD ["node", "server/index.js"]
EOF
  
  # Create docker-compose.yml
  cat > ./dist/docker-compose.yml << EOF
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
      - ai-service
    environment:
      - NODE_ENV=production
      - DB_HOST=db
      - DB_PORT=5432
      - DB_USERNAME=\${DB_USERNAME}
      - DB_PASSWORD=\${DB_PASSWORD}
      - DB_NAME=\${DB_NAME}
      - JWT_SECRET=\${JWT_SECRET}
      - AI_API_KEY=\${AI_API_KEY}
    volumes:
      - ./logs:/app/logs
    restart: always

  ai-service:
    build: ./ai
    ports:
      - "3001:3001"
    environment:
      - NODE_ENV=production
      - API_KEY=\${AI_API_KEY}
    volumes:
      - ./ai-models:/app/models
    restart: always

  db:
    image: postgres:14-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=\${DB_USERNAME}
      - POSTGRES_PASSWORD=\${DB_PASSWORD}
      - POSTGRES_DB=\${DB_NAME}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: always

volumes:
  postgres-data:
EOF
  
  # Create .dockerignore
  cat > ./dist/.dockerignore << EOF
node_modules
npm-debug.log
.git
.gitignore
.env
*.md
EOF
  
  log "Docker configuration created."
}

# Create deployment scripts
create_deployment_scripts() {
  log "Creating deployment scripts..."
  
  # Create deployment script
  cat > ./dist/deploy.sh << EOF
#!/bin/bash

# Deployment script for Unified Platform

# Set environment variables
export NODE_ENV=production

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Log function
log() {
  echo -e "\${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]\${NC} \$1"
}

error() {
  echo -e "\${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:\${NC} \$1"
}

# Check if .env file exists
if [ ! -f .env ]; then
  error ".env file not found. Please create .env file from .env.template."
  exit 1
fi

# Load environment variables
source .env

# Run database migrations
log "Running database migrations..."
node migrations/run-migrations.js

# Start application with Docker Compose
log "Starting application with Docker Compose..."
docker-compose up -d

# Check if application is running
log "Checking if application is running..."
sleep 5
if curl -s http://localhost:3000/api/health | grep -q "ok"; then
  log "Application is running successfully."
else
  error "Application failed to start. Check logs with 'docker-compose logs'."
  exit 1
fi

log "Deployment completed successfully."
EOF
  
  # Make deployment script executable
  chmod +x ./dist/deploy.sh
  
  # Create backup script
  cat > ./dist/backup.sh << EOF
#!/bin/bash

# Backup script for Unified Platform

# Set environment variables
export NODE_ENV=production

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Log function
log() {
  echo -e "\${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]\${NC} \$1"
}

error() {
  echo -e "\${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:\${NC} \$1"
}

# Load environment variables
source .env

# Create backup directory
BACKUP_DIR="./backups/\$(date +'%Y-%m-%d_%H-%M-%S')"
mkdir -p \$BACKUP_DIR

# Backup database
log "Backing up database..."
docker-compose exec db pg_dump -U \$DB_USERNAME \$DB_NAME > "\$BACKUP_DIR/database.sql"

# Backup uploaded files
log "Backing up uploaded files..."
tar -czf "\$BACKUP_DIR/uploads.tar.gz" ./uploads

# Backup configuration
log "Backing up configuration..."
cp .env "\$BACKUP_DIR/.env"
cp config/production.json "\$BACKUP_DIR/production.json"

log "Backup completed successfully. Backup stored in \$BACKUP_DIR"
EOF
  
  # Make backup script executable
  chmod +x ./dist/backup.sh
  
  log "Deployment scripts created."
}

# Create monitoring and health check scripts
create_monitoring_scripts() {
  log "Creating monitoring and health check scripts..."
  
  # Create health check script
  cat > ./dist/health-check.sh << EOF
#!/bin/bash

# Health check script for Unified Platform

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Log function
log() {
  echo -e "\${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]\${NC} \$1"
}

error() {
  echo -e "\${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:\${NC} \$1"
}

warn() {
  echo -e "\${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:\${NC} \$1"
}

# Check web service
log "Checking web service..."
if curl -s http://localhost:3000/api/health | grep -q "ok"; then
  log "Web service is running."
else
  error "Web service is not responding."
fi

# Check AI service
log "Checking AI service..."
if curl -s http://localhost:3001/health | grep -q "ok"; then
  log "AI service is running."
else
  error "AI service is not responding."
fi

# Check database connection
log "Checking database connection..."
if docker-compose exec db pg_isready -U \$DB_USERNAME -d \$DB_NAME; then
  log "Database connection is working."
else
  error "Database connection failed."
fi

# Check disk space
log "Checking disk space..."
DISK_USAGE=$(df -h | grep '/dev/sda1' | awk '{print \$5}' | sed 's/%//')
if [ \$DISK_USAGE -gt 90 ]; then
  error "Disk usage is critical: \${DISK_USAGE}%"
elif [ \$DISK_USAGE -gt 80 ]; then
  warn "Disk usage is high: \${DISK_USAGE}%"
else
  log "Disk usage is normal: \${DISK_USAGE}%"
fi

# Check memory usage
log "Checking memory usage..."
MEMORY_USAGE=$(free | grep Mem | awk '{print \$3/\$2 * 100.0}' | cut -d. -f1)
if [ \$MEMORY_USAGE -gt 90 ]; then
  error "Memory usage is critical: \${MEMORY_USAGE}%"
elif [ \$MEMORY_USAGE -gt 80 ]; then
  warn "Memory usage is high: \${MEMORY_USAGE}%"
else
  log "Memory usage is normal: \${MEMORY_USAGE}%"
fi

log "Health check completed."
EOF
  
  # Make health check script executable
  chmod +x ./dist/health-check.sh
  
  log "Monitoring scripts created."
}

# Package application
package_application() {
  log "Packaging application..."
  
  # Create package directory
  mkdir -p ./package
  
  # Create package archive
  tar -czf ./package/unified-platform-production.tar.gz -C ./dist .
  
  log "Application packaged successfully: ./package/unified-platform-production.tar.gz"
}

# Create installation guide
create_installation_guide() {
  log "Creating installation guide..."
  
  # Create installation guide
  cat > ./package/INSTALL.md << EOF
# Unified Platform - Installation Guide

This guide provides instructions for deploying the Unified Platform in a production environment.

## Prerequisites

- Node.js 16 or higher
- npm 7 or higher
- Docker and Docker Compose
- PostgreSQL 14 or higher (if not using Docker)
- 4GB RAM minimum (8GB recommended)
- 20GB disk space minimum

## Installation Steps

1. **Extract the package**

   \`\`\`bash
   tar -xzf unified-platform-production.tar.gz -C /opt/unified-platform
   cd /opt/unified-platform
   \`\`\`

2. **Configure environment variables**

   \`\`\`bash
   cp .env.template .env
   # Edit .env file with your production values
   nano .env
   \`\`\`

3. **Deploy the application**

   \`\`\`bash
   ./deploy.sh
   \`\`\`

4. **Verify installation**

   \`\`\`bash
   ./health-check.sh
   \`\`\`

5. **Set up scheduled backups (optional)**

   Add to crontab:
   \`\`\`
   0 2 * * * /opt/unified-platform/backup.sh
   \`\`\`

## Updating the Application

1. Extract the new package to a temporary directory
2. Stop the current application: \`docker-compose down\`
3. Back up the current installation: \`./backup.sh\`
4. Copy the new files to the installation directory
5. Run database migrations: \`node migrations/run-migrations.js\`
6. Start the application: \`docker-compose up -d\`

## Troubleshooting

- **Application fails to start**: Check logs with \`docker-compose logs\`
- **Database connection issues**: Verify database credentials in .env file
- **Performance issues**: Run \`./health-check.sh\` to check resource usage

## Support

For support, contact support@unifiedplatform.com or visit our support portal at https://support.unifiedplatform.com.
EOF
  
  # Copy installation guide to package
  cp ./package/INSTALL.md ./package/
  
  log "Installation guide created."
}

# Main function
main() {
  log "Starting production deployment package creation..."
  
  # Check requirements
  check_requirements
  
  # Clean build directories
  clean_build
  
  # Install dependencies
  install_dependencies
  
  # Build frontend
  build_frontend
  
  # Build backend
  build_backend
  
  # Build AI services
  build_ai_services
  
  # Prepare configuration files
  prepare_config
  
  # Prepare database migration scripts
  prepare_migrations
  
  # Create Docker configuration
  create_docker_config
  
  # Create deployment scripts
  create_deployment_scripts
  
  # Create monitoring scripts
  create_monitoring_scripts
  
  # Package application
  package_application
  
  # Create installation guide
  create_installation_guide
  
  log "Production deployment package created successfully!"
  log "Package location: ./package/unified-platform-production.tar.gz"
  log "Installation guide: ./package/INSTALL.md"
}

# Run main function
main
