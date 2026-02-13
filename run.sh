#!/bin/bash
# Quick start script for Resume Application System

echo "Resume Application System - Quick Start"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/installed.flag" ]; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
    touch venv/installed.flag
    echo "✓ Dependencies installed"
fi

# Run the application
echo ""
echo "Starting Resume Application System..."
echo ""
python src/main.py
