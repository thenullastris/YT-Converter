#!/bin/bash
set -e

echo "================================================"
echo "  YT Converter - AppImage Builder"
echo "================================================"

# Install appimage-builder if not present
if ! command -v appimage-builder &> /dev/null; then
    echo "📦 Installing appimage-builder..."
    sudo apt install -y appimage-builder
fi

# Clean previous build
rm -rf AppDir *.AppImage 2>/dev/null || true

# Build
echo "🔨 Building AppImage..."
appimage-builder --recipe AppImageBuilder.yml

echo ""
echo "✅ Done! Your AppImage is ready:"
ls -lh *.AppImage

echo ""
echo "To run it:"
echo "  chmod +x *.AppImage"
echo "  ./*.AppImage"