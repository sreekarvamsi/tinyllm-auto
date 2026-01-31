#!/bin/bash

# TinyLLM-Auto Quick Start Script
# This script sets up the project and guides you through first-time setup

set -e  # Exit on error

echo "======================================================================"
echo "🚗 TinyLLM-Auto - Quick Start Setup"
echo "======================================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip -q
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"
echo ""

# Check for model
echo "Checking for model file..."
if [ ! -f "models/phi-2-4bit.gguf" ]; then
    echo "⚠️  Model not found!"
    echo ""
    echo "To download the model:"
    echo "1. Visit: https://huggingface.co/TheBloke/phi-2-GGUF"
    echo "2. Download: phi-2.Q4_K_M.gguf"
    echo "3. Place in: models/phi-2-4bit.gguf"
    echo ""
    echo "Or use the automated downloader:"
    echo "   python scripts/download_model.py"
    echo ""
else
    echo "✓ Model found"
    echo ""
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p models data logs
echo "✓ Directories created"
echo ""

echo "======================================================================"
echo "✓ Setup Complete!"
echo "======================================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Download the model (if not already done):"
echo "   python scripts/download_model.py"
echo ""
echo "2. Run the CLI demo:"
echo "   python src/demo.py"
echo ""
echo "3. Or launch the web interface:"
echo "   python src/gradio_demo.py"
echo ""
echo "4. For voice interface, install additional dependencies:"
echo "   pip install openai-whisper TTS sounddevice soundfile"
echo ""
echo "Documentation:"
echo "   README.md - Project overview"
echo "   docs/APPLICATIONS.md - Use cases and applications"
echo "   docs/GITHUB_SETUP.md - GitHub setup guide"
echo ""
echo "======================================================================"
