#!/bin/bash
set -e

echo "================================================"
echo "  YT Converter - Setup & Run"
echo "================================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Install with: sudo apt install python3"
    exit 1
fi

# Check tkinter
python3 -c "import tkinter" 2>/dev/null || {
    echo "⚠️  tkinter not found. Installing..."
    sudo apt install -y python3-tk
}

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg not found. Installing..."
    sudo apt install -y ffmpeg
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install customtkinter yt-dlp --break-system-packages -q

# Run the app
echo "🚀 Launching YT Converter..."
python3 app.py