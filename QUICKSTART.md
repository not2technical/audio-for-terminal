# 🚀 Quick Start Guide

Get up and running with Voice Dictation in 5 minutes!

## 1. Clone the Repository

```bash
git clone https://github.com/not2technical/audio-for-terminal.git
cd audio-for-terminal
```

## 2. Install Dependencies

```bash
./setup.sh
```

This will:
- Install PortAudio via Homebrew
- Create a Python virtual environment
- Install all required Python packages
- Download the Whisper model

## 3. Configure API Key

```bash
./setup-access-key.sh
```

Follow the prompts to add your free Picovoice API key.

## 4. Grant Microphone Access

When prompted by macOS, click **Allow** to grant microphone access.

## 5. Start the Service

```bash
./toggle.sh
```

This starts the voice dictation service in the background.

## 6. Start Dictating!

```
1. Say "computer" (the wake word)
2. Speak your command or text
3. Pause briefly when done
4. Your text will be typed automatically!
```

## Example Session

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

## Common Commands

### Type Text
```
You: "computer"
You: "echo hello world"
→ Types: echo hello world
```

### Change Claude Mode
```
You: "computer"
You: "change mode"
→ Cycles through Claude's plan/edit/default modes
```

### Submit Input
```
You: "computer"
You: "send it"
→ Submits the command (press Enter)
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

## Troubleshooting

### Wake word not working?
- Speak clearly and at normal volume
- Try: `python main_streaming.py --sensitivity 0.7`
- Test with: `python wake_word_detector.py`

### Slow transcription?
- Use faster model: `python main_streaming.py --model tiny`
- Close other apps to free up CPU

### No audio captured?
- Test microphone: `python test_mic.py`
- Check System Settings → Privacy → Microphone

### Service not starting?
- Check status: `./status.sh`
- View logs: `tail -f /tmp/voice-dictation-streaming.log`
- Stop and restart: `./toggle.sh` twice

## Next Steps

- Read [README.md](README.md) for full documentation
- Explore all voice commands
- Customize wake word and settings
- Test individual components

---

**Need help?** Check the [README.md](README.md) for detailed troubleshooting.
