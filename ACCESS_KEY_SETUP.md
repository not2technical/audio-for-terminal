# 🔑 Picovoice Access Key Setup

> **⚠️ SECURITY NOTICE**
>
> **NEVER commit your API key to version control!**
>
> - The `.env` file is automatically excluded by `.gitignore`
> - Use `.env.example` as a template (no real keys in it)
> - Your API key is private - treat it like a password
> - If you accidentally commit a key, regenerate it immediately at https://console.picovoice.ai/

---

## Why Do I Need This?

Porcupine (the wake word detection engine) requires a **FREE** access key from Picovoice. This is a recent change to prevent abuse of their service.

✅ **100% FREE** for personal use
✅ **Still runs locally** - no cloud processing
✅ **Takes 2 minutes** to set up

---

## Step 1: Get Your FREE Access Key

1. **Go to:** https://console.picovoice.ai/
2. **Sign up** (free account)
3. **Copy your Access Key** from the dashboard

It looks like: `AbCdEf1234567890...` (40-50 characters)

---

## Step 2: Set the Access Key

Choose ONE of these methods:

### Method A: Environment Variable (Recommended) ⭐

Add to your shell config file:

**For zsh (default on macOS):**
```bash
echo 'export PICOVOICE_ACCESS_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**For bash:**
```bash
echo 'export PICOVOICE_ACCESS_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

Replace `your-key-here` with your actual key!

### Method B: .env File

Create a `.env` file in the voice-terminal directory:

```bash
cd voice-terminal
echo 'PICOVOICE_ACCESS_KEY=your-key-here' > .env
```

Then install python-dotenv:
```bash
source venv/bin/activate
pip install python-dotenv
```

### Method C: Pass as Command Line Argument

```bash
python main.py --access-key "your-key-here"
```

Or with the toggle script:
```bash
export PICOVOICE_ACCESS_KEY="your-key-here"
./toggle.sh
```

---

## Step 3: Verify It Works

```bash
cd voice-terminal
source venv/bin/activate
python main.py
```

You should see:
```
🎤 Voice Dictation for Terminal
============================================================

📦 Initializing components...
```

If it works, the wake word detector will start!

If you see an error about "access key required", go back to Step 2.

---

## Quick Test

```bash
cd voice-terminal
export PICOVOICE_ACCESS_KEY="your-key-here"
./run.sh
```

Then say **"computer"** to test!

---

## For Permanent Setup (Recommended)

1. Add to `~/.zshrc`:
   ```bash
   export PICOVOICE_ACCESS_KEY="your-actual-key-here"
   ```

2. Reload your shell:
   ```bash
   source ~/.zshrc
   ```

3. Now you can just run:
   ```bash
   ./toggle.sh
   ```

---

## Troubleshooting

**"Access key required" error?**
- Make sure you've set the environment variable
- Check if the key is correct (no extra quotes or spaces)
- Restart your terminal after adding to ~/.zshrc

**"Invalid access key" error?**
- Double-check you copied the full key from Picovoice Console
- Make sure there are no typos

**Still not working?**
```bash
# Check if environment variable is set:
echo $PICOVOICE_ACCESS_KEY

# Should show your key. If empty, it's not set correctly.
```

---

## Privacy & Security

✅ **Local Processing**: Your audio still never leaves your machine
✅ **Free Forever**: Personal use is free
✅ **No Credit Card**: Free tier doesn't require payment info
✅ **Open Source**: Porcupine is still Apache 2.0 licensed

The access key is just for analytics and to prevent abuse. All wake word detection happens locally on your computer.

---

## Alternative: Use a Different Wake Word Engine

If you prefer not to sign up, you can modify the code to use:
- Snowboy (deprecated but still works)
- Vosk (completely offline, no key needed)
- CMU PocketSphinx (older but stable)

Let me know if you'd like help setting up an alternative!

---

**Questions?** Check the main README.md or open an issue.
