#!/bin/bash

# Create a macOS Application Bundle for VoxTerm

APP_NAME="VoxTerm"
APP_DIR="$HOME/Applications/$APP_NAME.app"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "🎤 Creating macOS Application: $APP_NAME"
echo "==========================================="

# Create app bundle structure
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# Create Info.plist
cat > "$APP_DIR/Contents/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>VoxTerm</string>
    <key>CFBundleIdentifier</key>
    <string>com.voxterm.app</string>
    <key>CFBundleName</key>
    <string>VoxTerm</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSMicrophoneUsageDescription</key>
    <string>VoxTerm needs microphone access to listen for wake words and transcribe speech.</string>
</dict>
</plist>
PLIST

# Create launcher script
cat > "$APP_DIR/Contents/MacOS/VoxTerm" << LAUNCHER
#!/bin/bash

# VoxTerm Launcher

VOICE_DIR="$SCRIPT_DIR"

# Open a new Terminal window and run the app
osascript <<'EOF'
tell application "Terminal"
    activate
    set newTab to do script "cd '$SCRIPT_DIR' && source venv/bin/activate && python main.py"
end tell
EOF
LAUNCHER

# Make launcher executable
chmod +x "$APP_DIR/Contents/MacOS/VoxTerm"

# Create icon (optional - using emoji as text)
cat > "$APP_DIR/Contents/Resources/icon.txt" << 'ICON'
🎤
ICON

echo ""
echo "✅ Application created successfully!"
echo ""
echo "📍 Location: $APP_DIR"
echo ""
echo "🚀 To use:"
echo "   1. Open Finder"
echo "   2. Go to ~/Applications/"
echo "   3. Double-click VoxTerm.app"
echo ""
echo "💡 Tip: Drag VoxTerm.app to your Dock for quick access!"
echo ""
echo "🛑 To stop: Press Ctrl+C in the Terminal window"
echo ""
