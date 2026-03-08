# 🚀 Quick Launch Guide

Multiple ways to start/stop Voice Dictation without typing in terminal!

---

## Option 1: Toggle Script (Recommended) ⭐

**Start/Stop with one command:**

```bash
./toggle.sh
```

- First run = **Starts** voice dictation in background
- Second run = **Stops** voice dictation
- Runs silently in background
- Check logs: `/tmp/voice-dictation-streaming.log`

**Check if running:**
```bash
./status.sh
```

---

## Option 2: Create macOS App

**One-time setup:**
```bash
./create-app.sh
```

This creates `VoiceDictation.app` in `~/Applications/`

**To use:**
1. Open Finder → Go to `~/Applications/`
2. Double-click `VoiceDictation.app`
3. Terminal window opens and starts listening
4. Press `Ctrl+C` in that terminal to stop

**💡 Pro Tip:** Drag `VoiceDictation.app` to your Dock!

---

## Option 3: Keyboard Shortcut

### Using macOS Shortcuts (Built-in)

1. Open **Shortcuts.app** (built into macOS)
2. Click **+** to create new shortcut
3. Add action: **Run Shell Script**
4. Paste this script:
   ```bash
   cd /Users/akrys/audio-for-terminal && ./toggle.sh
   ```
5. Name it: "Toggle Voice Dictation"
6. Right-click → **Add Keyboard Shortcut**
7. Set to: `⌘⌥⇧V` (Cmd+Option+Shift+V)

Now press `⌘⌥⇧V` to start/stop voice dictation!

### Using Automator (Alternative)

1. Open **Automator.app**
2. New → **Quick Action**
3. Add: **Run Shell Script**
4. Paste:
   ```bash
   cd /Users/akrys/audio-for-terminal && ./toggle.sh
   ```
5. Save as: "Toggle Voice Dictation"
6. Go to: **System Settings → Keyboard → Keyboard Shortcuts**
7. Services → Find "Toggle Voice Dictation"
8. Add keyboard shortcut

---

## Option 4: Alfred/Raycast Integration

### Alfred Workflow
```bash
# Create Alfred workflow that runs:
cd /Users/akrys/audio-for-terminal && ./toggle.sh
```

**Trigger:** `voice` or `vd`

### Raycast Script Command
```bash
#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Toggle Voice Dictation
# @raycast.mode compact

cd /Users/akrys/audio-for-terminal && ./toggle.sh
```

Save as: `toggle-voice-dictation.sh` in Raycast script commands folder

---

## Option 5: Menu Bar Integration (Advanced)

Want a menu bar icon to start/stop? Here's how:

### Using BitBar/SwiftBar (Free)

1. Install SwiftBar: `brew install swiftbar`
2. Create plugin file:

```bash
#!/bin/bash
# <swiftbar.title>Voice Dictation</swiftbar.title>
# <swiftbar.version>v1.0</swiftbar.version>
# <swiftbar.author>You</swiftbar.author>

PID_FILE="/Users/akrys/audio-for-terminal/.voice-dictation-streaming.pid"

if [ -f "$PID_FILE" ] && ps -p "$(cat $PID_FILE)" > /dev/null 2>&1; then
    echo "🎤"
    echo "---"
    echo "Voice Dictation: Running ✅"
    echo "Stop | bash=/Users/akrys/audio-for-terminal/toggle.sh terminal=false refresh=true"
else
    echo "🎤"
    echo "---"
    echo "Voice Dictation: Stopped ❌"
    echo "Start | bash=/Users/akrys/audio-for-terminal/toggle.sh terminal=false refresh=true"
fi

echo "---"
echo "Status | bash=/Users/akrys/audio-for-terminal/status.sh terminal=true"
echo "Open Logs | bash='tail -f /tmp/voice-dictation-streaming.log' terminal=true"
```

3. Save to SwiftBar plugins folder
4. Click menu bar icon to start/stop!

---

## Option 6: Auto-Start on Login

### Make it start automatically when you log in:

1. Open **System Settings → General → Login Items**
2. Click **+** under "Open at Login"
3. Navigate to `~/Applications/VoiceDictation.app`
4. Click **Open**

Now voice dictation starts automatically when you log in!

**To disable:** Remove from Login Items

---

## How to Stop Voice Dictation

### Method 1: Toggle Script
```bash
./toggle.sh   # Runs stop if already running
```

### Method 2: Keyboard Interrupt
```bash
# In the terminal where it's running:
Press Ctrl+C
```

### Method 3: Status Check + Kill
```bash
./status.sh   # Shows PID
kill <PID>    # Replace <PID> with the number shown
```

### Method 4: Kill All Instances
```bash
pkill -f "python main_streaming.py"
```

### Method 5: Close Terminal Window
Just close the terminal window (less graceful)

---

## Comparison

| Method | Speed | Background | Keyboard | Easy Stop |
|--------|-------|------------|----------|-----------|
| Toggle Script | ⚡⚡⚡ | ✅ Yes | ❌ No | ✅ Easy |
| macOS App | ⚡⚡ | ❌ No | ❌ No | ⚡ Ctrl+C |
| Keyboard Shortcut | ⚡⚡⚡ | ✅ Yes | ✅ Yes | ✅ Easy |
| Alfred/Raycast | ⚡⚡⚡ | ✅ Yes | ⚡ Cmd+Space | ✅ Easy |
| Menu Bar | ⚡⚡⚡ | ✅ Yes | ❌ No | ✅ Click |
| Auto-Start | ⚡⚡⚡ | ✅ Yes | ❌ No | ⚡ Toggle |

---

## Recommended Setup

**For most users:**
1. Use `./toggle.sh` for quick start/stop
2. Create keyboard shortcut (Option 3)
3. Or use Alfred/Raycast (Option 4)

**For power users:**
1. Install SwiftBar menu bar app (Option 5)
2. Add to Login Items (Option 6)
3. Set up keyboard shortcut as backup

**For simplicity:**
1. Run `./create-app.sh` once
2. Drag app to Dock
3. Click to start, Ctrl+C to stop

---

## Files Created

- `toggle.sh` - Start/stop in one command
- `status.sh` - Check if running
- `create-app.sh` - Creates macOS application
- `VoiceDictation.app.sh` - Simple launcher
- This guide - `LAUNCHER_GUIDE.md`

---

## Troubleshooting

**"Permission denied" when running scripts:**
```bash
chmod +x *.sh
```

**Can't find the app after creating:**
```bash
open ~/Applications/
```

**Want to see logs when running in background:**
```bash
tail -f /tmp/voice-dictation-streaming.log
```

**Check if it's actually running:**
```bash
./status.sh
```

---

**Questions? Check README.md or USAGE.md for more details!**
