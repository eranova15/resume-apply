#!/bin/bash
# Quick start script for Resume Application System

set -e  # Exit on error

echo "Resume Application System - Quick Start"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

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
