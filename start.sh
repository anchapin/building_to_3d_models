#!/bin/bash

# Start the backend server
echo "Starting backend server..."
cd deployment/api
python app.py &
BACKEND_PID=$!
cd ../..

# Wait for the backend to start
echo "Waiting for backend to start..."
sleep 3

# Start the frontend server
echo "Starting frontend server..."
cd frontend/building-to-3d-app
npm run dev &
FRONTEND_PID=$!
cd ../..

# Function to handle script termination
function cleanup {
  echo "Stopping servers..."
  kill $BACKEND_PID
  kill $FRONTEND_PID
  exit
}

# Register the cleanup function for script termination
trap cleanup SIGINT SIGTERM

# Keep the script running
echo "Both servers are running. Press Ctrl+C to stop."
wait