#!/bin/bash

# Voice Dictation Launcher Script

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Check if model argument provided
if [ "$1" == "tiny" ] || [ "$1" == "base" ] || [ "$1" == "small" ] || [ "$1" == "medium" ] || [ "$1" == "large" ]; then
    MODEL="--model $1"
else
    MODEL="--model base"
fi

# Check if wake word provided
if [ ! -z "$2" ]; then
    WAKE_WORD="--wake-word $2"
else
    WAKE_WORD="--wake-word computer"
fi

echo ""
echo "🎤 Starting Voice Dictation for Terminal"
echo "=========================================="
echo ""

# Run the main app
python main.py $MODEL $WAKE_WORD

# Deactivate when done
deactivate
