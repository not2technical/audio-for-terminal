#!/bin/bash

# Voice Dictation Toggle Script - Now uses STREAMING mode by default
# (Regular mode has been deprecated - streaming is faster and better)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "ℹ️  Note: toggle.sh now launches STREAMING mode (faster, real-time transcription)"
echo ""

# Just call the streaming toggle script
exec "$SCRIPT_DIR/toggle-streaming.sh" "$@"
