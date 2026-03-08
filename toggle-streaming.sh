#!/bin/bash

# Toggle Voice Dictation STREAMING mode

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="$SCRIPT_DIR/.voice-dictation-streaming.pid"

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        # Already running - stop it
        echo "🛑 Stopping Voice Dictation Streaming (PID: $PID)..."
        kill "$PID" 2>/dev/null
        rm -f "$PID_FILE"
        echo "✅ Voice Dictation Streaming stopped"
        exit 0
    else
        # PID file exists but process is not running
        rm -f "$PID_FILE"
    fi
fi

# Not running - start it
echo "🚀 Starting Voice Dictation STREAMING mode..."

# Check if access key is set, if not try to load from ~/.zshrc
if [ -z "$PICOVOICE_ACCESS_KEY" ]; then
    if [ -f ~/.zshrc ]; then
        source ~/.zshrc
    fi
fi

# Check again after sourcing
if [ -z "$PICOVOICE_ACCESS_KEY" ]; then
    echo ""
    echo "⚠️  Warning: PICOVOICE_ACCESS_KEY environment variable not set"
    echo "   Please add to ~/.zshrc:"
    echo "   export PICOVOICE_ACCESS_KEY='your-key-here'"
    echo ""
    exit 1
fi

cd "$SCRIPT_DIR"
source venv/bin/activate

# Start in background
PICOVOICE_ACCESS_KEY="$PICOVOICE_ACCESS_KEY" python -u main_streaming.py > /tmp/voice-dictation-streaming.log 2>&1 &
PID=$!
echo $PID > "$PID_FILE"

echo "✅ Voice Dictation Streaming started (PID: $PID)"
echo "📝 Log file: /tmp/voice-dictation-streaming.log"
echo ""
echo "🎤 Say 'computer' to activate"
echo "✨ Text will appear AS YOU SPEAK"
echo "🛑 Run this script again to stop"
echo ""
echo "💡 Tip: Watch logs with: tail -f /tmp/voice-dictation-streaming.log"
echo ""
