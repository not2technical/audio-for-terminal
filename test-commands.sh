#!/bin/bash

# Test what Whisper transcribes for various commands

echo "🧪 Command Transcription Test"
echo "=============================="
echo ""
echo "This will help debug why commands work intermittently."
echo ""
echo "Watch /tmp/voice-dictation.log to see:"
echo "  1. What Whisper transcribes (📝 Raw transcription)"
echo "  2. Whether commands are detected (🎯 Command detected)"
echo ""
echo "Common issues:"
echo "  • Whisper might transcribe 'move left' as 'muv left' or 'move laughed'"
echo "  • Background noise can affect recognition"
echo "  • Speaking too fast/slow"
echo ""
echo "Try saying these commands and watch the log:"
echo ""
echo "  ✓ 'move left'"
echo "  ✓ 'move right'"
echo "  ✓ 'move to start'"
echo "  ✓ 'move to end'"
echo "  ✓ 'delete word'"
echo "  ✓ 'delete line'"
echo "  ✓ 'press enter'"
echo ""
echo "Starting log viewer..."
echo ""

tail -f /tmp/voice-dictation.log
