# 🎤 Voice Dictation - Quick Reference

## Start the App
```bash
cd audio-for-terminal && ./toggle.sh
```

## Monitor Service Logs
```bash
tail -f /tmp/voice-dictation-streaming.log
```

## How to Use
1. Say **"computer"** (wake word)
2. Speak your command
3. Pause briefly when done
4. Text types automatically!

## Voice Commands Cheat Sheet

### 🎯 Claude Mode Toggle
| Say This | Action |
|----------|--------|
| "change mode" | Cycle through Claude's plan/edit/default modes |
| "change mode twice" | Cycle through modes twice |
| "change mode three times" | Cycle three times |

### 📤 Text Submission
| Say This | Action |
|----------|--------|
| "send it" | Submit the current input (press Enter) |
| "submit" | Submit the current input (press Enter) |

### 📝 Text Input
| Say This | Result |
|----------|--------|
| "echo hello world" | `echo hello world` |
| "git status" | `git status` |
| Just speak naturally | Text types as you speak |

### ⬅️➡️ Navigation
| Say This | Action |
|----------|--------|
| "move left" | Move cursor left 1 |
| "move left 5" | Move cursor left 5 |
| "move right 3" | Move cursor right 3 |
| "move to start" | Jump to line start |
| "move to end" | Jump to line end |
| "beginning" | Jump to line start |

### ✂️ Editing
| Say This | Action |
|----------|--------|
| "delete word" | Delete previous word |
| "delete line" | Clear entire line |
| "delete" | Delete 1 character |
| "delete 3" | Delete 3 characters |
| "backspace" | Delete 1 character |

## Common Workflows

### Simple Text Entry
```
"computer"
"echo hello world"
"computer"
"send it"
```

### Change Claude Mode
```
"computer"
"change mode"
[Mode cycles to next]
```

### Fix Typo
```
"computer"
"echo helo world"
[realizes typo]
"computer"
"move left 6"
"computer"
"delete"
"computer"
"ll"
```

### Use Editing Commands
```
"computer"
"this is some text"
[text appears]
"computer"
"delete word"
[last word removed]
"computer"
"new text here"
```

## Launch Options

### Background Service (Recommended)
```bash
./toggle.sh
```

### Foreground Mode (Testing)
```bash
./run-streaming.sh
```

### Fast Mode (Less Accurate)
```bash
python main_streaming.py --model tiny
```

### Accurate Mode (Slower)
```bash
python main_streaming.py --model small
```

### Custom Wake Word
```bash
python main_streaming.py --wake-word jarvis
```

Available wake words: **computer**, **jarvis**, **alexa**, **hey google**, **ok google**, **porcupine**, **bumblebee**, **terminator**

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Wake word not detected | Speak louder, increase sensitivity: `python main_streaming.py --sensitivity 0.7` |
| Slow transcription | Use tiny model: `python main_streaming.py --model tiny` |
| Wrong text | Speak slower, use better model: `python main_streaming.py --model small` |
| No microphone | Grant permissions in System Settings |
| Text not appearing | Make sure terminal has focus |
| Service not running | Check: `./status.sh`, view logs: `tail -f /tmp/voice-dictation-streaming.log` |

## Test Components

```bash
source venv/bin/activate

python test_mic.py           # Test microphone
python wake_word_detector.py # Test wake word (say "computer")
python audio_recorder.py     # Test recording
python input_injector.py     # Test typing
```

## Stop the App

### Background Service
```bash
./toggle.sh  # Toggles off
```

### Foreground Mode
Press `Ctrl+C`

---

**Print this page for quick reference! 🖨️**
