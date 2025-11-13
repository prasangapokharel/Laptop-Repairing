#!/bin/bash
echo "========================================"
echo "Starting Backend Server..."
echo "========================================"
echo ""

# Change to backend directory
cd "$(dirname "$0")/backend"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Start backend server using run.py
echo "Starting FastAPI server on http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 run.py

