#!/bin/bash

# Run Voice Dictation with Overlay in a new Terminal window

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if access key is set
if [ -z "$PICOVOICE_ACCESS_KEY" ]; then
    # Try to load from .zshrc
    if [ -f "$HOME/.zshrc" ]; then
        source "$HOME/.zshrc"
    fi
fi

# Create a temporary script to run in the new terminal
TEMP_SCRIPT=$(mktemp)
cat > "$TEMP_SCRIPT" << 'RUNSCRIPT'
#!/bin/bash

# Load environment
if [ -f "$HOME/.zshrc" ]; then
    source "$HOME/.zshrc"
fi

# Navigate to voice-terminal
cd "SCRIPT_DIR_PLACEHOLDER"

# Activate virtual environment
source venv/bin/activate

# Check for access key
if [ -z "$PICOVOICE_ACCESS_KEY" ]; then
    echo ""
    echo "⚠️  Error: PICOVOICE_ACCESS_KEY not found"
    echo ""
    echo "Please add to ~/.zshrc:"
    echo "  export PICOVOICE_ACCESS_KEY='your-key-here'"
    echo ""
    echo "Then run: source ~/.zshrc"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

# Run with GUI overlay
echo ""
echo "🎤 Starting Voice Dictation with Overlay..."
echo ""
python main.py

# Keep window open if it crashes
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Voice Dictation exited with an error"
    echo ""
    read -p "Press Enter to close..."
fi
RUNSCRIPT

# Replace placeholder with actual script directory
sed -i.bak "s|SCRIPT_DIR_PLACEHOLDER|$SCRIPT_DIR|g" "$TEMP_SCRIPT"
chmod +x "$TEMP_SCRIPT"

# Open new Terminal window and run the script
osascript <<EOF
tell application "Terminal"
    activate
    do script "$TEMP_SCRIPT"
end tell
EOF

# Clean up after a delay
(sleep 2 && rm -f "$TEMP_SCRIPT" "$TEMP_SCRIPT.bak") &

echo "✅ Voice Dictation launched in new Terminal window"
echo "   You should see the blue pulsing overlay when you say 'computer'"
echo ""
