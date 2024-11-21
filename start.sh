#!/bin/bash

# Exit on error
set -e

# Project directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start Redis if not running
if ! brew services list | grep redis | grep started > /dev/null; then
    echo "Starting Redis..."
    brew services start redis
fi

# Function to start a process in the background
start_process() {
    local name=$1
    local command=$2
    echo "Starting $name..."
    $command &
    sleep 2  # Give each process time to start
}

# Create logs directory if it doesn't exist
mkdir -p logs

# Start Flask app
start_process "Flask app" "flask run --port=5001 --debug"

# Start Celery worker
start_process "Celery worker" "celery --app celery_app worker --loglevel=info"

# Start Celery beat
start_process "Celery beat" "celery --app celery_app beat --loglevel=info"

# Function to cleanup background processes on script exit
cleanup() {
    echo
    echo "Stopping all processes..."
    pkill -f "flask" || true
    pkill -f "celery" || true
    echo "All processes stopped"
    exit 0
}

# Register cleanup function to run on script exit
trap cleanup SIGINT SIGTERM

# Keep the script running until Ctrl+C is pressed
echo "All services started. Press Ctrl+C to stop all services."
while true; do
    sleep 1
done
