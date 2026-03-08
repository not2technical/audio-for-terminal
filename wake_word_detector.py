"""
Wake word detection using Porcupine
"""
import pyaudio
import struct
import pvporcupine
import os


class WakeWordDetector:
    def __init__(self, wake_word="computer", sensitivity=0.5, access_key=None):
        """
        Initialize wake word detector

        Args:
            wake_word: The wake word to detect. Built-in options include:
                       "alexa", "americano", "blueberry", "bumblebee",
                       "computer", "grapefruit", "grasshopper", "hey google",
                       "hey siri", "jarvis", "ok google", "picovoice",
                       "porcupine", "terminator"
            sensitivity: Detection sensitivity (0.0 to 1.0)
            access_key: Picovoice access key (get free at https://console.picovoice.ai/)
                       Can also be set via PICOVOICE_ACCESS_KEY environment variable
        """
        self.wake_word = wake_word
        self.sensitivity = sensitivity
        self.porcupine = None
        self.audio = None
        self.stream = None
        self.running = False

        # Get access key from parameter or environment
        self.access_key = access_key or os.getenv('PICOVOICE_ACCESS_KEY')

        if not self.access_key:
            print("\n" + "="*70)
            print("⚠️  PICOVOICE ACCESS KEY REQUIRED")
            print("="*70)
            print("\nPorcupine requires a FREE access key from Picovoice.")
            print("\n📝 To get your FREE access key:")
            print("   1. Go to: https://console.picovoice.ai/")
            print("   2. Sign up (it's free!)")
            print("   3. Copy your Access Key")
            print("\n🔑 Then set it one of these ways:")
            print("   • Environment variable:")
            print("     export PICOVOICE_ACCESS_KEY='your-key-here'")
            print("   • Or pass to script:")
            print("     python main.py --access-key 'your-key-here'")
            print("   • Or create .env file:")
            print("     echo 'PICOVOICE_ACCESS_KEY=your-key-here' > .env")
            print("\n" + "="*70 + "\n")
            raise ValueError("Picovoice access key is required. See instructions above.")

    def start(self, callback):
        """
        Start listening for wake word

        Args:
            callback: Function to call when wake word is detected
        """
        try:
            # Validate wake word is available
            wake_word_lower = self.wake_word.lower()
            if wake_word_lower not in pvporcupine.KEYWORDS:
                print(f"⚠️  Wake word '{self.wake_word}' not found.")
                print(f"Available wake words: {', '.join(sorted(pvporcupine.KEYWORDS))}")
                wake_word_lower = "computer"
                print(f"Using default: {wake_word_lower}")

            # Initialize Porcupine
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keywords=[wake_word_lower],
                sensitivities=[self.sensitivity]
            )

            # Initialize PyAudio
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

            print(f"🎧 Listening for wake word: '{self.wake_word}'...")
            print(f"   (Say '{self.wake_word}' to activate)")

            self.running = True

            # Listen for wake word
            while self.running:
                pcm = self.stream.read(
                    self.porcupine.frame_length,
                    exception_on_overflow=False
                )
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

                keyword_index = self.porcupine.process(pcm)

                if keyword_index >= 0:
                    print(f"\n🔔 Wake word detected: '{self.wake_word}'")
                    callback()

        except Exception as e:
            print(f"❌ Error in wake word detection: {e}")
        finally:
            self.stop()

    def stop(self):
        """Stop listening for wake word"""
        self.running = False

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        if self.audio:
            self.audio.terminate()
            self.audio = None

        if self.porcupine:
            self.porcupine.delete()
            self.porcupine = None


# Test the wake word detector
if __name__ == "__main__":
    import time

    def on_wake_word():
        print("✅ Wake word callback triggered!")
        time.sleep(2)  # Simulate some processing

    detector = WakeWordDetector(wake_word="computer")

    try:
        print("\n" + "="*60)
        print("Wake Word Detector Test")
        print("="*60)
        print("\nAvailable wake words:")
        print("  - computer (recommended)")
        print("  - jarvis")
        print("  - alexa")
        print("  - hey google")
        print("  - ok google")
        print("  - porcupine")
        print("  - bumblebee")
        print("  - terminator")
        print("\n" + "="*60 + "\n")

        detector.start(callback=on_wake_word)

    except KeyboardInterrupt:
        print("\n\n👋 Stopping wake word detector...")
        detector.stop()
