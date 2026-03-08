# 🚀 Streaming Mode - Real-Time Voice Dictation

## What's New?

**STREAMING MODE** - Text appears **AS YOU SPEAK**!

No more waiting for silence → transcribe → type. Text now flows in real-time!

---

## 🆚 Comparison: Standard vs Streaming

| Feature | Standard Mode | Streaming Mode |
|---------|---------------|----------------|
| **Response time** | 4-5 seconds after speaking | **Real-time as you speak** ⚡ |
| **How it works** | Wait for silence → transcribe all → type | Transcribe chunks → type immediately |
| **Latency** | High (wait for complete audio) | **Low (0.5-1s per word)** |
| **Best for** | Commands, short phrases | Long dictation, continuous speech |
| **CPU usage** | Moderate | Slightly higher |

---

## 🚀 Quick Start

### Stop standard mode (if running):
```bash
./toggle.sh  # Stop standard mode
```

### Start streaming mode:

**Option 1: Foreground (see output)**
```bash
./run-streaming.sh
```

**Option 2: Background**
```bash
./toggle-streaming.sh
```

---

## 💡 How It Works

### Standard Mode Flow:
```
Say "computer" → Speak → Silence (2s) → Transcribe (2s) → Type
Total: ~4-5 seconds after you stop speaking
```

### Streaming Mode Flow:
```
Say "computer" → Speak word 1 → Types word 1 (0.5s) → Speak word 2 → Types word 2 (0.5s) → ...
Text appears WHILE you're still speaking! ⚡
```

---

## 🎯 What to Expect

### Before (Standard):
```
You: "computer"
You: "echo hello world"
[pause 2 seconds]
[transcribing 2 seconds]
Terminal: echo hello world   ← Appears all at once
```

### After (Streaming):
```
You: "computer"
You: "echo"     → Terminal: echo
You: "hello"    → Terminal: echo hello
You: "world"    → Terminal: echo hello world
Text appears word-by-word as you speak! ✨
```

---

## 📝 Commands

### Start Streaming Mode:
```bash
# Foreground (recommended for testing)
./run-streaming.sh

# Background
./toggle-streaming.sh
```

### Stop Streaming Mode:
```bash
# If running in foreground
Ctrl+C

# If running in background
./toggle-streaming.sh
```

### View Logs:
```bash
tail -f /tmp/voice-dictation-streaming.log
```

### Check Status:
```bash
ps aux | grep main_streaming
```

---

## ⚙️ Configuration

### Use Faster Model (Recommended):
```bash
./run-streaming.sh --model tiny
```

The `tiny` model is **perfect for streaming** because:
- Faster transcription (less lag)
- Lower CPU usage
- Still very accurate for dictation

### Custom Wake Word:
```bash
./run-streaming.sh --wake-word jarvis
```

---

## 🔧 How Streaming Works (Technical)

1. **Audio Chunking**: Records audio in 0.5-second chunks
2. **Continuous Transcription**: Each chunk is transcribed immediately
3. **Real-time Typing**: Words are typed as soon as they're transcribed
4. **Silence Detection**: Stops after 2.5 seconds of silence

**Key Technology:**
- Uses `faster-whisper` instead of standard `openai-whisper`
- Optimized for low-latency streaming
- Processes audio in parallel with recording

---

## 💡 Tips for Best Results

### 1. Use Tiny Model for Speed:
```bash
./toggle-streaming.sh --model tiny
```

### 2. Speak Continuously:
- Streaming works best with continuous speech
- Short pauses are OK (< 2 seconds)
- Long pauses (> 2.5s) will end recording

### 3. Clear Speech:
- Speak at normal pace
- Clear enunciation helps accuracy
- Background noise affects streaming more

### 4. For Long Dictation:
Streaming mode is **much better** for:
- Long emails
- Code comments
- Documentation
- Continuous typing

---

## 🐛 Troubleshooting

### Issue: Text appears slowly
**Solution:** Use tiny model
```bash
./toggle-streaming.sh --model tiny
```

### Issue: Words are cut off
**Cause:** Silence detection too aggressive
**Solution:** Streaming uses 2.5s silence (vs 2.0s in standard)

### Issue: High CPU usage
**Solution:**
- Use tiny model (much less CPU)
- Close other applications
- Standard mode uses less CPU if needed

### Issue: Less accurate than standard
**Cause:** Streaming sacrifices some accuracy for speed
**Solution:**
- Use `base` or `small` model (slower but more accurate)
- Or use standard mode for important dictation

---

## 📊 Performance

### Model Comparison (Streaming):

| Model | Speed | Accuracy | CPU | Recommended For |
|-------|-------|----------|-----|-----------------|
| **tiny** | ⚡⚡⚡ Very Fast | ⭐⭐⭐ Good | 🔋 Low | **Streaming** ⭐ |
| **base** | ⚡⚡ Fast | ⭐⭐⭐⭐ Very Good | 🔋🔋 Medium | Balanced |
| **small** | ⚡ Slower | ⭐⭐⭐⭐⭐ Excellent | 🔋🔋🔋 High | Accuracy |

**Recommendation for streaming: `tiny` model**

---

## 🔄 Switching Between Modes

### Use Streaming Mode:
```bash
./toggle.sh             # Stop standard
./toggle-streaming.sh   # Start streaming
```

### Use Standard Mode:
```bash
./toggle-streaming.sh   # Stop streaming
./toggle.sh             # Start standard
```

### Can't run both at once!
Only one mode can run at a time (both listen for the same wake word).

---

## 🎯 When to Use Each Mode

### Use Streaming Mode When:
- ✅ Dictating long text
- ✅ Writing emails, docs, code
- ✅ You want immediate feedback
- ✅ You speak continuously

### Use Standard Mode When:
- ✅ Giving short commands
- ✅ Need maximum accuracy
- ✅ CPU resources limited
- ✅ Background mode is important

---

## 🚀 Quick Commands Reference

```bash
# Start streaming (foreground)
./run-streaming.sh

# Start streaming (background)
./toggle-streaming.sh

# Stop streaming
./toggle-streaming.sh  # or Ctrl+C

# View logs
tail -f /tmp/voice-dictation-streaming.log

# Use tiny model (fastest)
./run-streaming.sh --model tiny
```

---

## ✨ Example Usage

### Long Dictation:
```bash
./run-streaming.sh --model tiny

Say: "computer"
Say: "This is a long sentence that I want to type and I can see
     each word appearing as I speak which is really cool and makes
     the experience much more interactive and responsive"

Watch words appear in real-time! ✨
```

### Code Comments:
```bash
Say: "computer"
Say: "hash this function calculates the fibonacci sequence using
     dynamic programming for optimal performance"

Result: # This function calculates the fibonacci sequence using
        dynamic programming for optimal performance
```

---

## 🎉 Summary

**Streaming mode = Text appears AS YOU SPEAK!**

- ⚡ **Much faster** - no more waiting for silence
- ✨ **Real-time feedback** - see words immediately
- 🎯 **Better for long dictation** - continuous flow
- 🚀 **Modern experience** - like professional voice typing

Try it now:
```bash
./run-streaming.sh --model tiny
```

Say "computer" and start speaking! 🎤

---

**Questions? Check logs:** `tail -f /tmp/voice-dictation-streaming.log`
