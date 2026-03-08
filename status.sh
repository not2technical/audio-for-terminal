#!/bin/bash

# Check Voice Dictation status (streaming mode only)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="$SCRIPT_DIR/.voice-dictation-streaming.pid"

echo ""
echo "🎤 Voice Dictation Status (Streaming Mode)"
echo "==========================================="
echo ""

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "✅ Status: RUNNING"
        echo "🔢 PID: $PID"
        echo "⏱️  Uptime: $(ps -p $PID -o etime= | xargs)"
        echo "💾 Memory: $(ps -p $PID -o rss= | awk '{printf "%.1f MB", $1/1024}')"
        echo ""
        echo "🛑 To stop: ./toggle.sh  (or ./toggle-streaming.sh)"
    else
        echo "⚠️  Status: STOPPED (stale PID file)"
        rm -f "$PID_FILE"
        echo ""
        echo "🚀 To start: ./toggle.sh"
    fi
else
    echo "❌ Status: STOPPED"
    echo ""
    echo "🚀 To start: ./toggle.sh"
fi

echo ""
echo "📝 Log: tail -f /tmp/voice-dictation-streaming.log"
echo ""
