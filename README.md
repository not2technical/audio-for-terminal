# 🎤 Audio for Terminal

**Privacy-focused voice dictation for terminal input with wake word activation and local speech-to-text.**

Type with your voice in any terminal application. Say "computer", speak your command, and watch it appear in your terminal. All processing happens locally on your machine - no cloud APIs, no privacy concerns.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

---

## 🎯 Why This Project?

- **🙌 Hands-Free Terminal Input** - Type long commands without touching the keyboard
- **🔒 Privacy First** - All speech recognition runs locally via OpenAI Whisper
- **⚡ Fast & Efficient** - Wake word activation means no wasted processing
- **♿ Accessibility** - Alternative input method for those who need it
- **🎪 Just Cool** - Because talking to your computer is the future

---

## ✨ Key Features

- **Wake Word Detection** - Say "computer" to activate (customizable)
- **Real-Time Streaming** - Instant transcription with faster-whisper
- **Voice Commands** - Navigate and edit with voice ("delete word", "send it", etc.)
- **Claude Mode Toggle** - Switch between plan/edit/default modes with voice
- **Background Service** - Run as daemon with toggle script
- **Configurable Models** - From tiny (fast) to large (accurate)

---

## 🏗️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Audio Capture** | PyAudio (16kHz, 16-bit PCM) |
| **Wake Word** | Porcupine (Picovoice) - requires free API key |
| **Speech Recognition** | OpenAI Whisper (local/offline) |
| **Streaming STT** | faster-whisper (real-time transcription) |
| **VAD** | WebRTC Voice Activity Detection |
| **Keyboard Simulation** | pynput |
| **GUI** | tkinter |
| **ML Framework** | PyTorch |

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/not2technical/audio-for-terminal.git
cd audio-for-terminal

# 2. Run setup script (installs dependencies)
./setup.sh

# 3. Configure your Picovoice API key (free)
./setup-access-key.sh

# 4. Start the background service
./toggle.sh
```

Say **"computer"**, then speak your command!

---

## 📋 Prerequisites

- **macOS** (tested on macOS 14+)
- **Python 3.9+**
- **Homebrew** (for installing PortAudio)
- **Microphone** access
- **Picovoice Access Key** (free tier available)

---

## 🔑 Getting Your Picovoice API Key

The wake word detection (Porcupine) requires a free API key from Picovoice:

1. **Visit**: https://console.picovoice.ai/
2. **Sign up** for a free account (no credit card required)
3. **Create** a new access key
4. **Copy** the key

Then run our automated setup:
```bash
./setup-access-key.sh
```

Or manually create a `.env` file:
```bash
cp .env.example .env
# Edit .env and paste your key
```

**Important**:
- The key is stored locally in `.env` (excluded from git)
- Only the wake word detection uses this key
- Speech-to-text (Whisper) runs 100% locally

See [ACCESS_KEY_SETUP.md](ACCESS_KEY_SETUP.md) for detailed instructions.

---

## 📦 Installation

### Automated Setup (Recommended)

```bash
./setup.sh
```

This script will:
- Create a Python virtual environment
- Install PortAudio via Homebrew
- Install all Python dependencies
- Download the Whisper model

### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install PortAudio
brew install portaudio

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: First run will download the Whisper model (~140MB for base model).

---

## 🎮 Usage

### Background Service (Recommended)

Start/stop as background service:
```bash
./toggle.sh
```

Run again to toggle off.

### Foreground Mode

Run in foreground for testing/debugging:
```bash
./run-streaming.sh
```

Press Ctrl+C to stop.

### Monitoring Background Service

View logs in real-time:
```bash
tail -f /tmp/voice-dictation-streaming.log
```

Shows wake word detections, transcriptions, command executions, and errors.

### Custom Configuration

```bash
# Use a different wake word
python main_streaming.py --wake-word jarvis

# Use a different model
python main_streaming.py --model small

# Adjust sensitivity
python main_streaming.py --sensitivity 0.7
```

---

## 🎤 Voice Commands

### Text Input
Just speak normally:
```
You: "computer"
You: "echo hello world"
→ Types: echo hello world
```

### Claude Mode Toggle

| Command | Action |
|---------|--------|
| `change mode` | Cycle through Claude's plan/edit/default modes |
| `change mode twice` | Cycle through modes twice |
| `change mode three times` | Cycle three times |

### Text Submission

| Command | Action |
|---------|--------|
| `send it` | Submit the current input (press Enter) |
| `submit` | Submit the current input (press Enter) |

### Navigation Commands

| Command | Action |
|---------|--------|
| `move left [N]` | Move cursor left N positions (default: 1) |
| `move right [N]` | Move cursor right N positions |
| `move to start` | Jump to start of line |
| `move to end` | Jump to end of line |
| `beginning` | Jump to start of line |

### Editing Commands

| Command | Action |
|---------|--------|
| `delete word` | Delete previous word |
| `delete line` | Delete entire line |
| `delete [N]` | Delete N characters (default: 1) |
| `backspace [N]` | Delete N characters |

See [CHEATSHEET.md](CHEATSHEET.md) for the complete command reference.

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 5 minutes
- **[USAGE.md](USAGE.md)** - Detailed usage instructions
- **[STREAMING_GUIDE.md](STREAMING_GUIDE.md)** - Streaming mode deep dive
- **[ACCESS_KEY_SETUP.md](ACCESS_KEY_SETUP.md)** - API key setup guide
- **[CHEATSHEET.md](CHEATSHEET.md)** - Voice commands reference
- **[LAUNCHER_GUIDE.md](LAUNCHER_GUIDE.md)** - Advanced launcher options

---

## 🏛️ Architecture

```
┌─────────────────────┐
│  Wake Word Detector │  (Porcupine)
│  "computer"         │
└──────────┬──────────┘
           │ Activated!
           ▼
┌─────────────────────┐
│  Audio Recorder     │  (PyAudio + WebRTC VAD)
│  Record until       │
│  silence detected   │
└──────────┬──────────┘
           │ Audio data
           ▼
┌─────────────────────┐
│  Transcriber        │  (OpenAI Whisper - Local)
│  Speech → Text      │  (or faster-whisper)
└──────────┬──────────┘
           │ Transcribed text
           ▼
┌─────────────────────┐
│  Command Processor  │  (Parse commands vs text)
│  "move left" → cmd  │
│  "hello" → text     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Input Injector     │  (pynput)
│  Simulate keyboard  │
└─────────────────────┘
```

---

## 📂 Project Structure

```
audio-for-terminal/
├── main_streaming.py          # Streaming mode entry point
├── streaming_recorder.py      # Real-time audio recording
├── streaming_transcriber.py   # faster-whisper transcription
├── wake_word_detector.py      # Porcupine wake word detection
├── input_injector.py          # Keyboard simulation
├── audio_recorder.py          # Audio recording with VAD
├── transcriber.py             # Whisper transcription
├── test_mic.py               # Microphone testing utility
├── setup.sh                   # Automated installation
├── setup-access-key.sh        # API key configuration
├── run-streaming.sh           # Launch streaming mode (foreground)
├── toggle.sh                  # Start/stop service (background)
├── toggle-streaming.sh        # Streaming service toggle
├── status.sh                  # Check service status
└── requirements.txt           # Python dependencies
```

---

## 🔒 Security & Privacy

- ✅ **All transcription happens locally** - No cloud APIs for speech-to-text
- ✅ **Picovoice key only used for wake word** - Not for transcription
- ✅ **Audio never leaves your machine** - 100% local processing
- ✅ **No telemetry** - No usage data collected
- ✅ **Open source** - Audit the code yourself

Your `.env` file containing the API key is automatically excluded from git via `.gitignore`. Never commit API keys to version control.

---

## 🐛 Troubleshooting

### Issue: "No module named 'pyaudio'"

**Solution:**
```bash
brew install portaudio
pip install pyaudio
```

### Issue: "Permission denied" for microphone

**Solution:**
1. Go to **System Settings → Privacy & Security → Microphone**
2. Enable microphone access for Terminal or your terminal app

### Issue: Wake word not detecting

**Solution:**
1. Speak clearly and at normal volume
2. Increase sensitivity: `python main_streaming.py --sensitivity 0.7`
3. Test microphone: `./test_mic.py`
4. Try different wake word: `python main_streaming.py --wake-word jarvis`

### Issue: Slow transcription

**Solution:**
1. Use streaming mode: `./run-streaming.sh`
2. Use smaller model: `python main_streaming.py --model tiny`
3. Close other applications to free up CPU/RAM

### Testing Microphone

**Solution:**
```bash
cd audio-for-terminal
source venv/bin/activate
python test_mic.py
```
Speaks a test sound and shows audio levels. Press Ctrl+C to stop.

---

## 🛠️ Advanced Usage

### Toggle On/Off

```bash
# Start or stop the service
./toggle-streaming.sh

# Check status
./status.sh
```

### Create macOS Application

```bash
./create-app.sh
```

Creates a `VoiceDictation.app` that you can add to your Dock.

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Before submitting:**
- Test your changes thoroughly
- Update documentation if needed
- Ensure no API keys in code

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

Free to use for personal and commercial projects.

---

## 🙏 Credits & Acknowledgments

- **[OpenAI Whisper](https://github.com/openai/whisper)** - Local speech recognition
- **[Picovoice Porcupine](https://picovoice.ai/)** - Wake word detection
- **[faster-whisper](https://github.com/guillaumekln/faster-whisper)** - Optimized Whisper inference
- **[PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)** - Audio capture
- **[pynput](https://github.com/moses-palmer/pynput)** - Keyboard simulation
- **[WebRTC VAD](https://github.com/wiseman/py-webrtcvad)** - Voice activity detection

---

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/not2technical/audio-for-terminal/issues)
- **Discussions**: [GitHub Discussions](https://github.com/not2technical/audio-for-terminal/discussions)

---

## ⭐ Show Your Support

If you find this project useful, please consider giving it a star on GitHub! It helps others discover the project.

---

**Made with ❤️ for the command line**

*Talk to your terminal. It's listening.*
