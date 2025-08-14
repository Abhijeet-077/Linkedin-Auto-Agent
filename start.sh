#!/bin/bash

echo "🚀 LinkedIn Auto Agent"
echo "====================="
echo ""

# Check for busy ports and kill processes
echo "🔍 Checking for busy ports..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
echo ""

# Start Backend Server
echo "🔧 Starting Backend Server (FastAPI)..."
cd Backend
python3 working_server.py &
BACKEND_PID=$!
cd ..
echo ""

# Start Frontend Server
echo "🎨 Starting Frontend Development Server (React + Vite)..."
cd Frontend
npm run dev &
FRONTEND_PID=$!
cd ..
echo ""

echo "✅ Both servers are starting..."
echo "🔗 Backend API: http://localhost:8000"
echo "🔗 Frontend App: http://localhost:8080"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
