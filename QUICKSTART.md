# 🚀 Quick Start Guide

Get up and running with Voice Dictation in 5 minutes!

## 1. Install Dependencies

```bash
cd voice-terminal
./setup.sh
```

This will:
- Install PortAudio via Homebrew
- Create a Python virtual environment
- Install all required Python packages

## 2. Activate Virtual Environment

```bash
source venv/bin/activate
```

## 3. Run the App

```bash
python main.py
```

## 4. Grant Microphone Access

When prompted by macOS, click **Allow** to grant microphone access.

## 5. Start Dictating!

```
1. Say "computer" (the wake word)
2. A blue pulsing circle will appear
3. Speak your command or text
4. Pause for 1.5 seconds when done
5. Your text will be typed automatically!
```

## Example Session

```
Terminal: $

You:      "computer"
          [Blue circle appears]

You:      "list all files"
          [Circle turns purple - processing]

Terminal: $ ls -la█
```

## Common Commands

### Type Text
```
You: "computer"
You: "echo hello world"
→ Types: echo hello world
```

### Navigate Cursor
```
You: "computer"
You: "move left 5"
→ Moves cursor left 5 positions
```

### Delete Text
```
You: "computer"
You: "delete word"
→ Deletes previous word
```

### Press Enter
```
You: "computer"
You: "press enter"
→ Executes the command
```

## Troubleshooting

### Wake word not working?
- Speak clearly and at normal volume
- Try: `python main.py --sensitivity 0.7`
- Test with: `python wake_word_detector.py`

### Slow transcription?
- Use faster model: `python main.py --model tiny`
- Close other apps to free up CPU

### No audio captured?
- Test microphone: `python audio_recorder.py`
- Check System Settings → Privacy → Microphone

## Next Steps

- Read [README.md](README.md) for full documentation
- Explore all voice commands
- Customize wake word and settings
- Test individual components

---

**Need help?** Check the [README.md](README.md) for detailed troubleshooting.
