#!/bin/bash

# Run Voice Dictation in STREAMING mode (types as you speak!)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$SCRIPT_DIR"
source venv/bin/activate

# Check for access key
if [ -z "$PICOVOICE_ACCESS_KEY" ]; then
    # Try to load from .zshrc
    if [ -f "$HOME/.zshrc" ]; then
        source "$HOME/.zshrc"
    fi
fi

if [ -z "$PICOVOICE_ACCESS_KEY" ]; then
    echo ""
    echo "⚠️  PICOVOICE_ACCESS_KEY not set"
    echo "   Run: source ~/.zshrc"
    echo ""
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║         🎤 STREAMING MODE - Types as you speak! ⚡       ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Run streaming version
python -u main_streaming.py "$@"
