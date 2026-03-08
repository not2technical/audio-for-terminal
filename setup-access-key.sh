#!/bin/bash

# Interactive Access Key Setup Script

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║       🔑 Picovoice Access Key Setup                           ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Detect shell
SHELL_NAME=$(basename "$SHELL")
if [ "$SHELL_NAME" = "zsh" ]; then
    RC_FILE="$HOME/.zshrc"
elif [ "$SHELL_NAME" = "bash" ]; then
    RC_FILE="$HOME/.bashrc"
else
    RC_FILE="$HOME/.profile"
fi

echo "📋 Step 1: Get Your FREE Access Key"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Open your browser and go to:"
echo "   👉 https://console.picovoice.ai/"
echo ""
echo "2. Sign up (it's free!)"
echo ""
echo "3. Copy your Access Key from the dashboard"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Press Enter when you have your access key ready..."
echo ""

echo "🔑 Step 2: Enter Your Access Key"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Paste your access key here: " ACCESS_KEY

if [ -z "$ACCESS_KEY" ]; then
    echo ""
    echo "❌ No access key provided. Exiting."
    echo ""
    exit 1
fi

echo ""
echo "💾 Step 3: Save Access Key"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Choose where to save your access key:"
echo ""
echo "  1) $RC_FILE (Recommended - permanent)"
echo "  2) Current session only (temporary)"
echo "  3) .env file in voice-terminal directory"
echo ""
read -p "Enter choice [1-3]: " CHOICE

case $CHOICE in
    1)
        # Add to RC file
        echo "" >> "$RC_FILE"
        echo "# Picovoice Access Key for Voice Dictation" >> "$RC_FILE"
        echo "export PICOVOICE_ACCESS_KEY=\"$ACCESS_KEY\"" >> "$RC_FILE"
        echo ""
        echo "✅ Access key added to $RC_FILE"
        echo ""
        echo "📝 To activate it now, run:"
        echo "   source $RC_FILE"
        echo ""
        echo "   Or restart your terminal"
        echo ""

        # Also export for current session
        export PICOVOICE_ACCESS_KEY="$ACCESS_KEY"
        ;;

    2)
        # Export for current session only
        export PICOVOICE_ACCESS_KEY="$ACCESS_KEY"
        echo ""
        echo "✅ Access key set for current session"
        echo ""
        echo "⚠️  Note: This will be lost when you close the terminal"
        echo ""
        ;;

    3)
        # Save to .env file
        SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
        echo "PICOVOICE_ACCESS_KEY=$ACCESS_KEY" > "$SCRIPT_DIR/.env"
        echo ""
        echo "✅ Access key saved to $SCRIPT_DIR/.env"
        echo ""
        echo "📝 Installing python-dotenv..."
        source "$SCRIPT_DIR/venv/bin/activate"
        pip install python-dotenv --quiet
        echo "✅ python-dotenv installed"
        echo ""

        # Also need to update main.py to load .env
        echo "⚠️  Note: You'll need to add code to load .env in main.py"
        echo ""
        ;;

    *)
        echo ""
        echo "❌ Invalid choice. Exiting."
        echo ""
        exit 1
        ;;
esac

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🧪 Step 4: Test It"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Would you like to test the setup now? [Y/n]: " TEST_CHOICE

if [[ "$TEST_CHOICE" =~ ^[Yy]$|^$ ]]; then
    echo ""
    echo "🚀 Starting Voice Dictation..."
    echo ""
    cd "$SCRIPT_DIR" 2>/dev/null || cd "$(dirname "$0")"
    source venv/bin/activate
    python main.py
else
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "To start Voice Dictation, run:"
    echo "   cd voice-terminal"
    echo "   ./run.sh"
    echo ""
    echo "Or use:"
    echo "   ./toggle.sh    # Start/stop in background"
    echo ""
fi
