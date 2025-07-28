#!/bin/bash
# Start the unified platform demo

# Check if port 3001 is already in use
if lsof -Pi :3001 -sTCP:LISTEN -t >/dev/null ; then
    echo "Port 3001 is already in use. Terminating the process..."
    kill -9 $(lsof -Pi :3001 -sTCP:LISTEN -t)
    sleep 2
fi

# Install backend dependencies
cd backend
npm install
node server.js &
BACKEND_PID=$!

# Start frontend
# Check if frontend directory exists
if [ -d "../frontend" ]; then
    cd ../frontend
    npm install
    npm start &
    FRONTEND_PID=$!
else
    echo "Frontend directory not found. Using built frontend..."
    # Use the frontend directory within demo-build
    cd ./frontend 2>/dev/null || echo "No local frontend directory found. Using backend-served static files."
    FRONTEND_PID=""
fi

echo "Demo started!"
echo "Backend running on http://localhost:3001"
echo "Frontend accessible at http://localhost:3001"

# Handle shutdown
function cleanup {
  echo "Shutting down demo services..."
  kill $BACKEND_PID 2>/dev/null
  if [ ! -z "$FRONTEND_PID" ]; then
    kill $FRONTEND_PID 2>/dev/null
  fi
  exit 0
}

trap cleanup SIGINT SIGTERM

# Keep script running
wait
