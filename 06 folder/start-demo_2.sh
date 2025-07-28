#!/bin/bash
# Start the unified platform demo

# Kill any existing node processes
pkill -f node || true
sleep 2

# Set production environment
export NODE_ENV=production

# Install backend dependencies
cd backend
npm install

# Start backend server (which will serve static frontend files)
echo "Starting backend server on port 3002..."
node server.js &
BACKEND_PID=$!

echo "Demo started!"
echo "Demo running on http://localhost:3002"

# Handle shutdown
function cleanup {
  echo "Shutting down demo services..."
  kill $BACKEND_PID
  exit 0
}
trap cleanup SIGINT SIGTERM

# Keep script running
wait
