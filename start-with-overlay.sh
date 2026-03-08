#!/bin/bash

# Simple launcher that opens a new terminal with the overlay

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load environment variables from .env file
if [ -f "$SCRIPT_DIR/.env" ]; then
    source "$SCRIPT_DIR/.env"
else
    echo "❌ Error: .env file not found"
    echo "Run ./setup-access-key.sh to configure your Picovoice API key"
    exit 1
fi

# Verify API key is set
if [ -z "$PICOVOICE_ACCESS_KEY" ]; then
    echo "❌ Error: PICOVOICE_ACCESS_KEY not set in .env file"
    echo "Run ./setup-access-key.sh to configure your API key"
    exit 1
fi

# Create a command to run in the new terminal
COMMAND="cd '$SCRIPT_DIR' && source venv/bin/activate && source .env && python main.py"

# Open new Terminal window and run the command
osascript <<EOF
tell application "Terminal"
    activate
    do script "$COMMAND"
end tell
EOF

echo ""
echo "✅ Voice Dictation launched in new Terminal window!"
echo ""
echo "👀 Look for:"
echo "   • New Terminal window that just opened"
echo "   • Blue pulsing circle (bottom-right of screen) when you say 'computer'"
echo ""
echo "🎤 Try it:"
echo "   1. Say 'computer' (wake word)"
echo "   2. Watch for blue pulsing overlay"
echo "   3. Say your command (e.g., 'echo hello world')"
echo ""
echo "🛑 To stop: Press Ctrl+C in the Voice Dictation terminal window"
echo ""
