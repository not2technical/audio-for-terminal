"""
Speech-to-text transcription using OpenAI Whisper (local)
"""
import whisper
import numpy as np
import tempfile
import os
from pathlib import Path


class WhisperTranscriber:
    def __init__(self, model_name="base", device="cpu"):
        """
        Initialize Whisper transcriber

        Args:
            model_name: Whisper model size
                       - tiny: fastest, least accurate
                       - base: good balance (recommended)
                       - small: more accurate, slower
                       - medium: very accurate, much slower
                       - large: most accurate, very slow
            device: "cpu" or "cuda"
        """
        self.model_name = model_name
        self.device = device
        self.model = None

        print(f"📥 Loading Whisper model '{model_name}'...")
        self._load_model()

    def _load_model(self):
        """Load the Whisper model"""
        try:
            self.model = whisper.load_model(self.model_name, device=self.device)
            print(f"✅ Whisper model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading Whisper model: {e}")
            raise

    def transcribe_audio_data(self, audio_data, sample_rate=16000):
        """
        Transcribe raw audio data

        Args:
            audio_data: Raw audio bytes (16-bit PCM)
            sample_rate: Sample rate of audio data

        Returns:
            str: Transcribed text
        """
        if not audio_data:
            return ""

        try:
            # Convert bytes to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)

            # Convert to float32 and normalize
            audio_float = audio_array.astype(np.float32) / 32768.0

            # Transcribe
            print("🔄 Transcribing audio...")
            result = self.model.transcribe(
                audio_float,
                language="en",
                fp16=False  # Use fp32 for CPU
            )

            text = result["text"].strip()
            print(f"📝 Transcription: {text}")

            return text

        except Exception as e:
            print(f"❌ Error transcribing audio: {e}")
            return ""

    def transcribe_file(self, audio_file):
        """
        Transcribe audio from file

        Args:
            audio_file: Path to audio file

        Returns:
            str: Transcribed text
        """
        try:
            print(f"🔄 Transcribing file: {audio_file}")
            result = self.model.transcribe(
                audio_file,
                language="en",
                fp16=False
            )

            text = result["text"].strip()
            print(f"📝 Transcription: {text}")

            return text

        except Exception as e:
            print(f"❌ Error transcribing file: {e}")
            return ""


# Test the transcriber
if __name__ == "__main__":
    import sys

    print("\n" + "="*60)
    print("Whisper Transcriber Test")
    print("="*60 + "\n")

    # Check if audio file provided
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        if not os.path.exists(audio_file):
            print(f"❌ File not found: {audio_file}")
            sys.exit(1)

        transcriber = WhisperTranscriber(model_name="base")
        text = transcriber.transcribe_file(audio_file)

        print("\n" + "="*60)
        print("Result:")
        print("="*60)
        print(text)
        print("="*60 + "\n")

    else:
        print("Usage: python transcriber.py <audio_file.wav>")
        print("\nOr test with audio recorder:")
        print("  1. Run: python audio_recorder.py")
        print("  2. Record audio to /tmp/test_recording.wav")
        print("  3. Run: python transcriber.py /tmp/test_recording.wav")
