#!/bin/bash
# Nexus Web UI - Quick Start Script

set -e

echo "🚀 Nexus Super App - Quick Start"
echo "================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Dependencies check passed"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Python dependencies installed"
echo ""

# Install Node dependencies
echo "📦 Installing Node dependencies..."
cd web-ui
npm install
cd ..
echo "✅ Node dependencies installed"
echo ""

# Create data directory if it doesn't exist
mkdir -p data

echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "Option 1: Development Mode"
echo "  1. Start backend:  python -m uvicorn api.main:app --reload"
echo "  2. Start frontend: cd web-ui && npm run dev"
echo "  3. Open browser:  http://localhost:5173"
echo ""
echo "Option 2: Docker Mode"
echo "  docker-compose up -d"
echo ""
echo "Happy coding! 🚀"
