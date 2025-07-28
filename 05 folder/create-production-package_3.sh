#!/bin/bash

# Create Production Package Script
# This script builds and packages the unified platform for production deployment

echo "Starting production build process..."

# Set environment variables
export NODE_ENV=production

# Create build directory
BUILD_DIR="./build"
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# Build frontend
echo "Building frontend..."
cd ./private/src/frontend
npm run build
if [ $? -ne 0 ]; then
  echo "Frontend build failed. Exiting."
  exit 1
fi
echo "Frontend build completed successfully."

# Copy frontend build to production directory
echo "Copying frontend build to production directory..."
mkdir -p $BUILD_DIR/frontend
cp -r ./.next $BUILD_DIR/frontend/
cp -r ./public $BUILD_DIR/frontend/
cp ./next.config.js $BUILD_DIR/frontend/
cp ./package.json $BUILD_DIR/frontend/

# Return to root directory
cd ../../../

# Build backend
echo "Building backend..."
mkdir -p $BUILD_DIR/backend
cp -r ./private/src/backend/* $BUILD_DIR/backend/

# Copy AI services
echo "Copying AI services..."
mkdir -p $BUILD_DIR/ai
cp -r ./private/src/ai/* $BUILD_DIR/ai/

# Copy services
echo "Copying services..."
mkdir -p $BUILD_DIR/services
cp -r ./private/src/services/* $BUILD_DIR/services/

# Copy documentation
echo "Copying documentation..."
mkdir -p $BUILD_DIR/documentation
cp -r ./documentation/* $BUILD_DIR/documentation/

# Copy configuration files
echo "Copying configuration files..."
cp ./package.json $BUILD_DIR/
cp ./README.md $BUILD_DIR/

# Create production deployment scripts
echo "Creating deployment scripts..."
cat > $BUILD_DIR/start.sh << 'EOF'
#!/bin/bash
# Start the unified platform in production mode
export NODE_ENV=production

# Start backend server
cd backend
node server.js &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm start &
FRONTEND_PID=$!

# Handle shutdown
function cleanup {
  echo "Shutting down services..."
  kill $BACKEND_PID
  kill $FRONTEND_PID
  exit 0
}

trap cleanup SIGINT SIGTERM

# Keep script running
wait
EOF

chmod +x $BUILD_DIR/start.sh

# Create environment configuration
cat > $BUILD_DIR/.env << 'EOF'
# Production Environment Configuration
PORT=3000
API_PORT=3001
MONGODB_URI=mongodb://localhost:27017/unified_platform
JWT_SECRET=replace_with_secure_production_secret
AWS_REGION=us-east-1
S3_BUCKET=unified-platform-assets
EOF

echo "Creating validation script..."
cat > $BUILD_DIR/validate.sh << 'EOF'
#!/bin/bash
# Validate the production build

echo "Validating production build..."

# Check for required directories
for dir in frontend backend ai services documentation; do
  if [ ! -d "$dir" ]; then
    echo "Error: $dir directory is missing"
    exit 1
  fi
done

# Check for required files
for file in package.json start.sh .env; do
  if [ ! -f "$file" ]; then
    echo "Error: $file is missing"
    exit 1
  fi
done

# Validate frontend build
if [ ! -d "frontend/.next" ]; then
  echo "Error: Frontend build is missing"
  exit 1
fi

# Validate backend
if [ ! -f "backend/server.js" ]; then
  echo "Error: Backend server is missing"
  exit 1
fi

echo "Validation completed successfully!"
exit 0
EOF

chmod +x $BUILD_DIR/validate.sh

# Create production package
echo "Creating production package..."
PACKAGE_NAME="unified-platform-$(date +%Y%m%d-%H%M%S).zip"
cd $BUILD_DIR
zip -r ../$PACKAGE_NAME .
cd ..

echo "Production package created: $PACKAGE_NAME"
echo "Production build completed successfully!"
