#!/usr/bin/env python3
"""
Voice Dictation for Terminal - STREAMING VERSION
Real-time transcription that types as you speak
"""
import re
import threading
import time
import signal
import sys
import os

from wake_word_detector import WakeWordDetector
from streaming_recorder import StreamingRecorder
from streaming_transcriber import StreamingTranscriber
from input_injector import InputInjector


class VoiceDictationStreaming:
    def __init__(
        self,
        wake_word="computer",
        whisper_model="base",
        sensitivity=0.5,
        access_key=None
    ):
        """
        Initialize Streaming Voice Dictation App

        Args:
            wake_word: Wake word to activate dictation
            whisper_model: Whisper model size (tiny, base, small, medium, large)
            sensitivity: Wake word detection sensitivity (0.0 to 1.0)
            access_key: Picovoice access key
        """
        print("\n" + "="*60)
        print("🎤 Voice Dictation for Terminal - STREAMING MODE")
        print("="*60 + "\n")

        self.wake_word = wake_word
        self.running = True
        self.currently_transcribing = False

        # Initialize components
        print("📦 Initializing components...\n")

        self.wake_detector = WakeWordDetector(
            wake_word=wake_word,
            sensitivity=sensitivity,
            access_key=access_key
        )
        self.recorder = StreamingRecorder()
        self.transcriber = StreamingTranscriber(model_name=whisper_model)
        self.injector = InputInjector(delay=0.003)  # Even faster for streaming

        # Transcription state
        self.current_transcription = []
        self.transcription_lock = threading.Lock()

        # Command detection buffer
        self.command_buffer = []  # Store last 5 segments for multi-word commands
        self.command_buffer_size = 5

        # Stop flag for command-triggered shutdown
        self.should_stop_streaming = False

        print("\n✅ All components initialized!\n")
        print("💡 Streaming mode: Text will appear as you speak!\n")

    def on_wake_word_detected(self):
        """Callback when wake word is detected - SIMPLIFIED: No streaming, transcribe once"""
        if not self.running or self.currently_transcribing:
            return

        self.currently_transcribing = True

        try:
            print("\n🎙️  Listening (speak now)...")

            # Just record - don't stream transcription
            audio_data = self.recorder.record_streaming(
                chunk_callback=lambda x: None,
                silence_callback=None,
                should_stop_callback=lambda: self.should_stop_streaming,
                max_duration=30,
                silence_duration=1.5  # Balanced for natural speech
            )

            if not audio_data:
                print("⚠️  No speech detected")
                return

            print("🔄 Transcribing...")

            # Transcribe ONCE at the end
            text = self.transcriber.transcribe_complete(audio_data)

            if not text:
                print("⚠️  No transcription")
                return

            # Filter wake word from anywhere
            words = text.split()
            filtered_words = [w for w in words if w.strip('.,!?;:').lower() != self.wake_word.lower()]
            text = " ".join(filtered_words).strip()

            if not text:
                return

            print(f"📝 {text}")

            # Check for commands FIRST
            text_lower = text.lower()
            print(f"🔍 Checking commands for: '{text_lower}'")  # Debug
            if self._check_for_commands(text_lower):
                print("✅ Command executed")
            else:
                # Not a command - type it
                self.injector.type_text(text)

        except Exception as e:
            print(f"\n❌ Error: {e}\n")

        finally:
            self.currently_transcribing = False
            self.should_stop_streaming = False

    def on_audio_chunk(self, audio_data):
        """Called when audio chunk is available"""
        self.transcriber.add_audio_chunk(audio_data)

    def on_silence_detected(self):
        """Called when silence is detected"""
        print("🤫 Silence detected, finalizing...")

    def on_transcription_segment(self, text, is_final):
        """
        Called when transcription segment is available

        Args:
            text: Transcribed text segment
            is_final: Whether this is the final transcription
        """
        with self.transcription_lock:
            # Strip wake word from ANYWHERE in text (with punctuation)
            words = text.split()
            filtered_words = []
            for word in words:
                if word.strip('.,!?;:').lower() != self.wake_word.lower():
                    filtered_words.append(word)

            if not filtered_words:
                return  # Only wake word, ignore

            text = " ".join(filtered_words)
            text_lower = text.lower().strip()

            # Add to recent buffer for multi-word command detection
            self.command_buffer.append(text_lower)
            if len(self.command_buffer) > self.command_buffer_size:
                self.command_buffer.pop(0)

            # Check if this is a command (current + recent context)
            combined = " ".join(self.command_buffer)
            if self._check_for_commands(combined):
                print(f"🎯 Command: {text}")
                return  # Don't type commands

            # Not a command - type it
            self.current_transcription.append(text)
            marker = "✅" if is_final else "📝"
            print(f"{marker} {text}")
            self.injector.type_text(text + " ")

    def _check_for_commands(self, text):
        """Check if text is a command - SIMPLE VERSION"""

        # 1. SEND IT - submit input
        if 'send it' in text or 'submit' in text:
            print(f"🎯 Detected 'send it' command")
            self.injector.execute_command("enter")
            self.should_stop_streaming = True
            return True

        # 2. MODE TOGGLING - Shift+Tab cycles through plan/edit/default modes
        if 'change mode' in text:
            print(f"🎯 Detected 'change mode' command")
            # Check if "twice" or a number is specified
            times = 1  # Default to once
            if 'twice' in text:
                times = 2
            elif 'three times' in text or 'thrice' in text:
                times = 3
            else:
                # Extract number if present
                times = self._extract_number(text, default=1)

            print(f"🔄 Toggling mode {times} time(s)")
            # Execute shift_tab the specified number of times
            for _ in range(times):
                self.injector.execute_command("shift_tab")
            return True

        # 3. DELETE COMMANDS
        if 'delete line' in text or 'clear line' in text:
            self.injector.execute_command("delete_line")
            return True

        if 'delete word' in text:
            self.injector.execute_command("delete_word")
            return True

        # 4. NAVIGATION
        if 'move left' in text or 'go left' in text:
            self.injector.execute_command("move_left", 1)
            return True

        if 'move right' in text or 'go right' in text:
            self.injector.execute_command("move_right", 1)
            return True

        return False

    def _extract_number(self, text, default=1):
        """Extract a number from text"""
        import re
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else default

    def run(self):
        """Run the voice dictation app"""
        print("="*60)
        print(f"🎧 Say '{self.wake_word}' to start dictation")
        print("="*60)
        print("\n💡 Streaming Mode Features:")
        print("   ✨ Text appears AS YOU SPEAK")
        print("   ✨ Real-time transcription")
        print("   ✨ Faster response time")
        print("\n💡 Voice Commands:")
        print("   • 'change mode' - Cycle through plan/edit/default modes")
        print("   • 'change mode twice' - Change twice")
        print("   • 'send it' - Submit input (press Enter)")
        print("   • 'delete word/line' - Delete word or line")
        print("   • 'move left/right' - Move cursor")
        print("   • Or just speak to type text\n")
        print("🛑 Press Ctrl+C to quit\n")

        # Start wake word detection (blocking)
        try:
            self.wake_detector.start(callback=self.on_wake_word_detected)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the voice dictation app"""
        print("\n\n👋 Shutting down...\n")
        self.running = False
        self.wake_detector.stop()
        self.recorder.close()
        self.transcriber.stop_streaming()
        print("✅ Goodbye!\n")
        sys.exit(0)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Voice Dictation for Terminal - STREAMING MODE",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Streaming Mode: Text appears AS YOU SPEAK - much faster!

Examples:
  %(prog)s                     # Use defaults
  %(prog)s --model tiny        # Fastest model
  %(prog)s --wake-word jarvis  # Custom wake word

Available models (for streaming, tiny/base recommended):
  tiny   - Fastest (recommended for streaming)
  base   - Good balance
  small  - More accurate, slower
        """
    )

    parser.add_argument(
        "--wake-word",
        default="computer",
        help="Wake word to activate dictation (default: computer)"
    )

    parser.add_argument(
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base, recommend tiny for streaming)"
    )

    parser.add_argument(
        "--sensitivity",
        type=float,
        default=0.5,
        help="Wake word detection sensitivity 0.0-1.0 (default: 0.5)"
    )

    parser.add_argument(
        "--access-key",
        default=None,
        help="Picovoice access key (or set PICOVOICE_ACCESS_KEY env var)"
    )

    args = parser.parse_args()

    # Get access key from env if not provided
    access_key = args.access_key or os.getenv('PICOVOICE_ACCESS_KEY')

    # Create and run app
    app = VoiceDictationStreaming(
        wake_word=args.wake_word,
        whisper_model=args.model,
        sensitivity=args.sensitivity,
        access_key=access_key
    )

    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, lambda sig, frame: app.stop())

    # Run the app
    app.run()


if __name__ == "__main__":
    main()
