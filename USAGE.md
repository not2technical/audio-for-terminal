# 🎤 Usage Guide

## Running the App

### Option 1: Quick Start (Recommended)
```bash
cd voice-terminal
./run.sh
```

### Option 2: With Custom Model
```bash
./run.sh tiny          # Fastest
./run.sh base          # Balanced (default)
./run.sh small         # More accurate
```

### Option 3: With Custom Wake Word
```bash
./run.sh base jarvis   # Model + wake word
```

### Option 4: Manual (Full Control)
```bash
source venv/bin/activate
python main.py --wake-word computer --model base --sensitivity 0.5
```

## How It Works

1. **Start the app** - Run `./run.sh`
2. **Wait for prompt** - You'll see "🎧 Say 'computer' to start dictation"
3. **Say wake word** - Say "computer" clearly
4. **See overlay** - A blue pulsing circle appears (bottom-right)
5. **Speak** - Say your command or text
6. **Pause** - Wait 1.5 seconds when done
7. **Watch it type** - Your text appears in the terminal!

## Voice Commands

### 🔤 Typing Text
Just speak normally:
```
You:      "computer"
You:      "echo hello world"
Terminal: echo hello world█
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
"press enter"         → Submit command
"new line"            → Press Enter
"submit"              → Press Enter
"press tab"           → Auto-complete
"escape"              → Cancel
"cancel"              → Press Escape
```

## Real-World Examples

### Example 1: Creating a Directory
```
Terminal: $

You:      "computer"
You:      "mkdir my dash project"
Terminal: $ mkdir my-project█

You:      "computer"
You:      "press enter"
Terminal: $ mkdir my-project
          $█
```

### Example 2: Listing Files
```
You:      "computer"
You:      "ls dash la"
Terminal: $ ls -la█
```

### Example 3: Editing Command
```
You:      "computer"
You:      "git commit dash m quote test quote"
Terminal: $ git commit -m "test"█

You:      "computer"
You:      "move left 6"
Terminal: $ git commit -m█"test"

You:      "computer"
You:      "delete word"
Terminal: $ git commit -█"test"

You:      "computer"
You:      "push"
Terminal: $ git commit -push"test"█

You:      "computer"
You:      "move to end"
Terminal: $ git commit -push"test"█
```

## Tips & Tricks

### 🎯 Better Recognition
- Speak clearly at normal volume
- Say "dash" for "-"
- Say "dot" for "."
- Say "slash" for "/"
- Say "quote" for quotation marks
- Pause briefly between words

### 🏃 Faster Transcription
```bash
./run.sh tiny    # Use tiny model for speed
```

### 🎯 Better Accuracy
```bash
./run.sh small   # Use small model for accuracy
```

### 🔊 More Sensitive Wake Word
```bash
python main.py --sensitivity 0.7
```

### 🔇 Less Sensitive Wake Word
```bash
python main.py --sensitivity 0.3
```

### 🎭 Different Wake Word
```bash
python main.py --wake-word jarvis
```

Available: computer, jarvis, alexa, hey google, ok google, porcupine, bumblebee, terminator

## Testing Components

Before running the full app, test individual components:

### Test Microphone
```bash
source venv/bin/activate
python test_mic.py
```

### Test Wake Word Detection
```bash
source venv/bin/activate
python wake_word_detector.py
# Say "computer" to test
# Press Ctrl+C to stop
```

### Test Audio Recording
```bash
source venv/bin/activate
python audio_recorder.py
# Speak after the prompt
# Your audio is saved to /tmp/test_recording.wav
```

### Test Transcription
```bash
source venv/bin/activate
python audio_recorder.py
python transcriber.py /tmp/test_recording.wav
```

### Test Keyboard Input
```bash
source venv/bin/activate
python input_injector.py
# Focus your terminal within 3 seconds
# Watch it type test commands
```

## Troubleshooting

### Wake word not detected
- Speak louder and clearer
- Try: `python main.py --sensitivity 0.7`
- Check microphone with: `python test_mic.py`

### Transcription is slow
- Use faster model: `./run.sh tiny`
- Close other applications
- Check CPU usage

### Text not appearing
- Make sure terminal has focus
- Try clicking in the terminal before speaking
- Test with: `python input_injector.py`

### Overlay not showing
- Check if app is running
- Try running: `python overlay_ui.py`
- Ensure Python has accessibility permissions

### Wrong text transcribed
- Speak more slowly and clearly
- Use better model: `./run.sh small`
- Reduce background noise
- Get closer to microphone

## Stopping the App

Press `Ctrl+C` in the terminal running the app.

## Getting Help

- Read [README.md](README.md) for full documentation
- Check [QUICKSTART.md](QUICKSTART.md) for installation help
- Test components individually to isolate issues

---

**Enjoy hands-free terminal control! 🎤✨**
