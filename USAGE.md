# 🎤 Usage Guide

## Running the App

### Option 1: Background Service (Recommended)
```bash
cd audio-for-terminal
./toggle.sh     # Start or stop the service
```

This runs voice dictation as a background service. Run again to toggle off.

### Option 2: Foreground (for testing/debugging)
```bash
./run-streaming.sh     # Run in foreground, see live output
```

Press Ctrl+C to stop.

### Monitoring Background Service

When running via `./toggle.sh`, monitor the log file in real-time:
```bash
tail -f /tmp/voice-dictation-streaming.log
```

The log shows:
- Wake word detections ("computer" detected)
- Transcription results
- Command executions ("change mode", "send it", etc.)
- Errors and debugging info

Press Ctrl+C to stop watching (service continues running).

### Option 3: Direct Python Execution
```bash
source venv/bin/activate
python main_streaming.py
```

### Custom Configuration
```bash
# Use a different wake word
python main_streaming.py --wake-word jarvis

# Use a different model
python main_streaming.py --model small

# Adjust sensitivity
python main_streaming.py --sensitivity 0.7
```

## How It Works

1. **Start the app** - Run `./toggle.sh`
2. **Wait for prompt** - You'll see "🎧 Say 'computer' to start dictation" in the log
3. **Say wake word** - Say "computer" clearly
4. **Speak** - Say your command or text
5. **Pause** - Wait briefly when done
6. **Watch it type** - Your text appears in the terminal!

## Voice Commands

### 🔤 Typing Text
Just speak normally:
```
You:      "computer"
You:      "echo hello world"
Terminal: echo hello world█
```

### 🎯 Claude Mode Toggle
```
"change mode"         → Cycle through Claude's plan/edit/default modes
"change mode twice"   → Cycle through modes twice
"change mode three times" → Cycle three times
```

### 📤 Text Submission
```
"send it"             → Submit the current input (press Enter)
```

### ⬅️➡️ Cursor Navigation
```
"move left"           → Move left 1 position
"move left 5"         → Move left 5 positions
"move right 3"        → Move right 3 positions
"move to start"       → Jump to start of line
"move to end"         → Jump to end of line
"beginning"           → Jump to start of line
```

### ✂️ Editing
```
"delete word"         → Delete previous word
"delete line"         → Clear entire line
"delete"              → Delete 1 character
"delete 3"            → Delete 3 characters
"backspace"           → Delete 1 character
```

### ⌨️ Special Keys
```
"press enter"         → Press Enter
"new line"            → Press Enter
"press tab"           → Auto-complete
"escape"              → Cancel
"cancel"              → Press Escape
```

## Real-World Examples

### Example 1: Simple Text Entry
```
Terminal: $

You:      "computer"
You:      "echo hello world"
Terminal: $ echo hello world█

You:      "computer"
You:      "send it"
Terminal: $ echo hello world
          hello world
          $█
```

### Example 2: Editing Text
```
You:      "computer"
You:      "git status"
Terminal: $ git status█

You:      "computer"
You:      "delete word"
Terminal: $ git █

You:      "computer"
You:      "add all"
Terminal: $ git add all█
```

### Example 3: Using Change Mode
```
You:      "computer"
You:      "change mode"
Terminal: [Cycles through Claude's modes]

You:      "computer"
You:      "help me write a script"
Terminal: $ help me write a script█

You:      "computer"
You:      "send it"
Terminal: [Command submitted to Claude]
```

## Tips & Tricks

### 🎯 Better Recognition
- Speak clearly at normal volume
- Speak naturally - just say the text you want typed
- Pause briefly between commands
- Use "change mode" to switch Claude modes
- Use "send it" to submit input

### 🏃 Faster Transcription
```bash
python main_streaming.py --model tiny    # Use tiny model for speed
```

### 🎯 Better Accuracy
```bash
python main_streaming.py --model small   # Use small model for accuracy
```

### 🔊 More Sensitive Wake Word
```bash
python main_streaming.py --sensitivity 0.7
```

### 🔇 Less Sensitive Wake Word
```bash
python main_streaming.py --sensitivity 0.3
```

### 🎭 Different Wake Word
```bash
python main_streaming.py --wake-word jarvis
```

Available: computer, jarvis, alexa, hey google, ok google, porcupine, bumblebee, terminator

## Testing Components

Before running the full app, test individual components:

### Test Microphone
```bash
cd audio-for-terminal
source venv/bin/activate
python test_mic.py
```
Speaks a test sound and shows audio levels. Press Ctrl+C to stop.

### Test Wake Word Detection
```bash
cd audio-for-terminal
source venv/bin/activate
python wake_word_detector.py
# Say "computer" to test
# Press Ctrl+C to stop
```

### Test Audio Recording
```bash
cd audio-for-terminal
source venv/bin/activate
python audio_recorder.py
# Speak after the prompt
# Your audio is saved to /tmp/test_recording.wav
```

### Test Transcription
```bash
cd audio-for-terminal
source venv/bin/activate
python audio_recorder.py
python transcriber.py /tmp/test_recording.wav
```

### Test Keyboard Input
```bash
cd audio-for-terminal
source venv/bin/activate
python input_injector.py
# Focus your terminal within 3 seconds
# Watch it type test commands
```

## Troubleshooting

### Wake word not detected
- Speak louder and clearer
- Try: `python main_streaming.py --sensitivity 0.7`
- Check microphone with: `python test_mic.py`

### Transcription is slow
- Use faster model: `python main_streaming.py --model tiny`
- Close other applications
- Check CPU usage

### Text not appearing
- Make sure terminal has focus
- Try clicking in the terminal before speaking
- Test with: `python input_injector.py`

### Wrong text transcribed
- Speak more slowly and clearly
- Use better model: `python main_streaming.py --model small`
- Reduce background noise
- Get closer to microphone

### Service not running
- Check status: `./status.sh`
- Check logs: `tail -f /tmp/voice-dictation-streaming.log`
- Restart: `./toggle.sh` (off), then `./toggle.sh` (on)

## Stopping the App

- **Background service**: `./toggle.sh` (toggles off)
- **Foreground mode**: Press `Ctrl+C` in the terminal running the app

## Getting Help

- Read [README.md](README.md) for full documentation
- Check [QUICKSTART.md](QUICKSTART.md) for installation help
- Test components individually to isolate issues

---

**Enjoy hands-free terminal control! 🎤✨**
