#!/bin/bash

echo "=================================================="
echo "🎤 VoxTerm - Setup"
echo "=================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed."
    echo "   Install from: https://brew.sh"
    exit 1
fi

echo "✅ Homebrew found"
echo ""

# Install PortAudio
echo "📦 Installing PortAudio..."
if brew list portaudio &> /dev/null; then
    echo "   ✅ PortAudio already installed"
else
    brew install portaudio
    if [ $? -eq 0 ]; then
        echo "   ✅ PortAudio installed successfully"
    else
        echo "   ❌ Failed to install PortAudio"
        exit 1
    fi
fi
echo ""

# Create virtual environment
echo "🐍 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "   ✅ Virtual environment already exists"
else
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "   ✅ Virtual environment created"
    else
        echo "   ❌ Failed to create virtual environment"
        exit 1
    fi
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "   ✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet
echo "   ✅ pip upgraded"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
echo "   This may take a few minutes..."
echo ""

pip install pyaudio --quiet
echo "   ✅ PyAudio installed"

pip install openai-whisper --quiet
echo "   ✅ OpenAI Whisper installed"

pip install pynput --quiet
echo "   ✅ pynput installed"

pip install pvporcupine --quiet
echo "   ✅ Porcupine installed"

pip install webrtcvad --quiet
echo "   ✅ WebRTC VAD installed"

pip install numpy --quiet
echo "   ✅ NumPy installed"

pip install torch torchvision torchaudio --quiet
echo "   ✅ PyTorch installed"

echo ""
echo "=================================================="
echo "✅ Setup complete!"
echo "=================================================="
echo ""
echo "📝 Next steps:"
echo ""
echo "   1. Activate virtual environment:"
echo "      source venv/bin/activate"
echo ""
echo "   2. Run the app:"
echo "      python main.py"
echo ""
echo "   3. Say 'computer' to start dictation!"
echo ""
echo "=================================================="
echo "💡 Tips:"
echo "   • Use --help to see all options"
echo "   • Read README.md for detailed documentation"
echo "   • Test components individually before running main app"
echo "=================================================="
echo ""
