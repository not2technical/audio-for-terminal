"""
Real-time streaming transcription using faster-whisper
"""
from faster_whisper import WhisperModel
import numpy as np
import threading
import queue
import time


class StreamingTranscriber:
    def __init__(self, model_name="base", device="cpu"):
        """
        Initialize streaming transcriber

        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
            device: "cpu" or "cuda"
        """
        self.model_name = model_name
        self.device = device
        self.model = None

        print(f"📥 Loading faster-whisper model '{model_name}'...")
        self._load_model()

        # Streaming state
        self.audio_queue = queue.Queue()
        self.transcription_callback = None
        self.is_streaming = False
        self.stream_thread = None

        # Track previous transcription to avoid duplicates
        self.previous_text = []
        self.last_words = []

    def _load_model(self):
        """Load the faster-whisper model"""
        try:
            # Use int8 for faster performance on CPU
            self.model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type="int8"
            )
            print(f"✅ faster-whisper model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading faster-whisper model: {e}")
            raise

    def start_streaming(self, callback):
        """
        Start streaming transcription

        Args:
            callback: Function to call with each transcribed segment
                     callback(text: str, is_final: bool)
        """
        if self.is_streaming:
            print("⚠️  Already streaming")
            return

        # Reset deduplication state
        self.previous_text = []
        self.last_words = []

        self.transcription_callback = callback
        self.is_streaming = True

        # Start background transcription thread
        self.stream_thread = threading.Thread(
            target=self._transcription_worker,
            daemon=True
        )
        self.stream_thread.start()
        print("🎙️  Streaming transcription started")

    def stop_streaming(self):
        """Stop streaming transcription"""
        self.is_streaming = False
        if self.stream_thread:
            self.stream_thread.join(timeout=2.0)
        print("🛑 Streaming transcription stopped")

    def add_audio_chunk(self, audio_data, sample_rate=16000):
        """
        Add audio chunk for transcription

        Args:
            audio_data: Raw audio bytes (16-bit PCM)
            sample_rate: Sample rate of audio
        """
        if not self.is_streaming:
            return

        # Convert bytes to float32 numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        audio_float = audio_array.astype(np.float32) / 32768.0

        self.audio_queue.put((audio_float, sample_rate))

    def _remove_duplicates(self, text):
        """Remove duplicate words - SIMPLE VERSION"""

        # FIRST: Check if text duplicates itself (e.g., "hello world. hello world")
        # Split in half and check if both halves are the same
        words = text.split()
        half = len(words) // 2

        if half > 0:
            first_half = words[:half]
            second_half = words[half:half*2]  # Same length as first half

            # Compare without punctuation
            first_clean = [w.strip('.,!?;:').lower() for w in first_half]
            second_clean = [w.strip('.,!?;:').lower() for w in second_half]

            if first_clean == second_clean:
                # Text is duplicated within itself!
                words = first_half
                text = " ".join(words)

        # SECOND: Remove overlap with previous segment
        if not self.last_words:
            # First segment
            self.last_words = words[-5:]
            return text

        # Check how many words at start match end of last segment
        overlap = 0
        for i in range(1, min(len(self.last_words), len(words)) + 1):
            if self.last_words[-i:] == words[:i]:
                overlap = i

        # Remove overlapping words
        if overlap > 0:
            words = words[overlap:]

        # Update buffer
        self.last_words = (self.last_words + words)[-5:]

        return " ".join(words) if words else ""

    def _transcription_worker(self):
        """Background worker that transcribes audio chunks"""
        audio_buffer = []
        min_chunk_duration = 1.5  # Wait for more audio (better quality, less duplication)
        sample_rate = 16000

        while self.is_streaming:
            try:
                # Get audio chunk with timeout
                audio_chunk, sr = self.audio_queue.get(timeout=0.1)
                sample_rate = sr
                audio_buffer.append(audio_chunk)

                # Calculate total duration
                total_samples = sum(len(chunk) for chunk in audio_buffer)
                duration = total_samples / sample_rate

                # Transcribe when we have enough audio
                if duration >= min_chunk_duration:
                    # Concatenate all chunks
                    combined_audio = np.concatenate(audio_buffer)

                    # Transcribe WITHOUT internal VAD (we handle segmentation)
                    segments, info = self.model.transcribe(
                        combined_audio,
                        language="en",
                        beam_size=1,
                        vad_filter=False,  # Don't let Whisper segment - causes duplicates
                        condition_on_previous_text=False  # Don't use previous context
                    )

                    # Collect ALL text from all segments, then deduplicate once
                    all_text = " ".join(segment.text.strip() for segment in segments if segment.text.strip())

                    if all_text and self.transcription_callback:
                        # Deduplicate the combined text
                        deduplicated = self._remove_duplicates(all_text)
                        if deduplicated:
                            self.transcription_callback(deduplicated, False)

                    # Clear processed audio
                    audio_buffer = []

            except queue.Empty:
                # No audio available, check if we should finalize
                if audio_buffer and not self.is_streaming:
                    # Final transcription
                    combined_audio = np.concatenate(audio_buffer)
                    segments, info = self.model.transcribe(
                        combined_audio,
                        language="en",
                        beam_size=5,
                        vad_filter=False,
                        condition_on_previous_text=False
                    )

                    all_text = " ".join(segment.text.strip() for segment in segments if segment.text.strip())

                    if all_text and self.transcription_callback:
                        deduplicated = self._remove_duplicates(all_text)
                        if deduplicated:
                            self.transcription_callback(deduplicated, True)

                    audio_buffer = []

            except Exception as e:
                print(f"❌ Transcription error: {e}")
                continue

    def transcribe_complete(self, audio_data, sample_rate=16000):
        """
        Transcribe complete audio (non-streaming, for compatibility)

        Args:
            audio_data: Raw audio bytes (16-bit PCM)
            sample_rate: Sample rate

        Returns:
            str: Transcribed text
        """
        if not audio_data:
            return ""

        try:
            # Convert bytes to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            audio_float = audio_array.astype(np.float32) / 32768.0

            # Transcribe
            print("🔄 Transcribing audio...")
            segments, info = self.model.transcribe(
                audio_float,
                language="en",
                beam_size=5
            )

            # Concatenate all segments
            text = " ".join(segment.text.strip() for segment in segments)
            print(f"📝 Transcription: {text}")

            return text

        except Exception as e:
            print(f"❌ Error transcribing audio: {e}")
            return ""


# Test the streaming transcriber
if __name__ == "__main__":
    import sys

    print("\n" + "="*60)
    print("Streaming Transcriber Test")
    print("="*60 + "\n")

    def on_transcription(text, is_final):
        marker = "✅" if is_final else "📝"
        print(f"{marker} {text}")

    transcriber = StreamingTranscriber(model_name="base")

    print("\nTest 1: Complete transcription")
    print("-" * 60)

    # Would need actual audio file to test
    print("(Need audio file to test - use with main.py)")

    print("\n" + "="*60 + "\n")
