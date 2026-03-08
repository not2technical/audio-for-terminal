# 🎤 Voice Dictation - Quick Reference

## Start the App
```bash
cd voice-terminal && ./run.sh
```

## How to Use
1. Say **"computer"** (wake word)
2. Blue circle appears = listening
3. Speak your command
4. Pause 1.5 seconds when done
5. Text types automatically!

## Voice Commands Cheat Sheet

### 📝 Text Input
| Say This | Result |
|----------|--------|
| "ls dash la" | `ls -la` |
| "echo hello world" | `echo hello world` |
| "git commit dash m quote test quote" | `git commit -m "test"` |

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

### ⌨️ Special Keys
| Say This | Action |
|----------|--------|
| "press enter" | Press Enter |
| "new line" | Press Enter |
| "submit" | Press Enter |
| "press tab" | Press Tab |
| "escape" | Press Escape |
| "cancel" | Press Escape |

## Pronunciation Guide
| Symbol | Say |
|--------|-----|
| `-` | "dash" |
| `.` | "dot" |
| `/` | "slash" |
| `"` | "quote" |
| `_` | "underscore" |
| `@` | "at" |
| `#` | "hash" or "pound" |

## Common Workflows

### Create Directory
```
"computer"
"mkdir my dash project"
"press enter"
```

### Git Commit
```
"computer"
"git add dot"
"press enter"
"computer"
"git commit dash m quote initial commit quote"
"press enter"
```

### Navigate Files
```
"computer"
"cd projects slash voice dash terminal"
"press enter"
"computer"
"ls dash la"
"press enter"
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
"hello"
```

## Launch Options

### Default (Recommended)
```bash
./run.sh
```

### Fast Mode (Less Accurate)
```bash
./run.sh tiny
```

### Accurate Mode (Slower)
```bash
./run.sh small
```

### Custom Wake Word
```bash
./run.sh base jarvis
```

Available wake words: **computer**, **jarvis**, **alexa**, **hey google**, **ok google**, **porcupine**, **bumblebee**, **terminator**

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Wake word not detected | Speak louder, increase sensitivity: `python main.py --sensitivity 0.7` |
| Slow transcription | Use tiny model: `./run.sh tiny` |
| Wrong text | Speak slower, use better model: `./run.sh small` |
| No microphone | Grant permissions in System Settings |
| Text not appearing | Make sure terminal has focus |

## Test Components

```bash
source venv/bin/activate

python test_mic.py           # Test microphone
python wake_word_detector.py # Test wake word (say "computer")
python audio_recorder.py     # Test recording
python input_injector.py     # Test typing
```

## Stop the App
Press `Ctrl+C`

---

**Print this page for quick reference! 🖨️**
