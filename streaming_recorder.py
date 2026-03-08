"""
Streaming audio recorder with real-time chunking
"""
import pyaudio
import webrtcvad
import collections
import time
import threading


class StreamingRecorder:
    def __init__(
        self,
        sample_rate=16000,
        frame_duration=30,  # ms
        chunk_duration=0.5,  # seconds - send chunks this often
        vad_aggressiveness=3
    ):
        self.sample_rate = sample_rate
        self.frame_duration = frame_duration
        self.frame_size = int(sample_rate * frame_duration / 1000)
        self.chunk_duration = chunk_duration
        self.frames_per_chunk = int(chunk_duration * 1000 / frame_duration)
        self.vad = webrtcvad.Vad(2)  # Aggressiveness 2 (balanced for natural speech)

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.record_thread = None

    def start_stream(self):
        """Start the audio input stream"""
        if self.stream is None or not self.stream.is_active():
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.frame_size
            )

    def stop_stream(self):
        """Stop the audio input stream"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def record_streaming(
        self,
        chunk_callback,
        silence_callback=None,
        should_stop_callback=None,
        max_duration=30,
        silence_duration=2.0
    ):
        """
        Record audio with streaming chunks

        Args:
            chunk_callback: Called with audio chunks as they're recorded
                           callback(audio_data: bytes)
            silence_callback: Called when silence detected (optional)
            should_stop_callback: Callback to check if recording should stop
                                 callback() -> bool
            max_duration: Maximum recording duration
            silence_duration: Duration of silence to stop recording

        Returns:
            bytes: Complete audio data
        """
        self.start_stream()

        all_frames = []
        chunk_frames = []
        num_silence_frames = int(silence_duration * 1000 / self.frame_duration)
        ring_buffer = collections.deque(maxlen=num_silence_frames)

        triggered = False
        start_time = time.time()
        last_chunk_time = start_time

        print("🎤 Recording (streaming)... speak now")

        while time.time() - start_time < max_duration:
            # Check if external signal to stop
            if should_stop_callback and should_stop_callback():
                print("🛑 Stop signal received")
                break

            frame = self.stream.read(self.frame_size, exception_on_overflow=False)
            all_frames.append(frame)
            chunk_frames.append(frame)

            # Check if frame contains speech
            is_speech = self.vad.is_speech(frame, self.sample_rate)

            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])

                # Start recording when we detect speech
                if num_voiced > 0.3 * ring_buffer.maxlen:  # 30% threshold - enables short commands
                    triggered = True
                    print("🗣️  Speech detected, streaming...")
                    # Add buffered frames to chunk
                    for f, _ in ring_buffer:
                        chunk_frames.append(f)
                    ring_buffer.clear()
            else:
                # Already recording - check for chunks to send
                current_time = time.time()
                if current_time - last_chunk_time >= self.chunk_duration:
                    # Send chunk
                    if chunk_frames:
                        chunk_data = b''.join(chunk_frames)
                        chunk_callback(chunk_data)
                        chunk_frames = []
                        last_chunk_time = current_time

                # Check for silence
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])

                # Stop recording when silence detected
                if num_unvoiced > 0.8 * ring_buffer.maxlen:  # 80% silence (more tolerant)
                    print("🤫 Silence detected")

                    # Send final chunk
                    if chunk_frames:
                        chunk_data = b''.join(chunk_frames)
                        chunk_callback(chunk_data)

                    if silence_callback:
                        silence_callback()
                    break

        # If we never detected speech, return empty
        if not triggered:
            print("⚠️  No speech detected")
            return b''

        # Return complete audio
        audio_data = b''.join(all_frames)
        return audio_data

    def close(self):
        """Clean up resources"""
        self.stop_stream()
        self.audio.terminate()


# Test the streaming recorder
if __name__ == "__main__":
    recorder = StreamingRecorder()

    def on_chunk(audio_data):
        duration = len(audio_data) / (16000 * 2)
        print(f"📦 Chunk received: {duration:.2f}s ({len(audio_data)} bytes)")

    def on_silence():
        print("✅ Recording complete (silence detected)")

    try:
        print("Testing streaming recorder...")
        print("Speak continuously and watch chunks arrive...")
        print()

        audio_data = recorder.record_streaming(
            chunk_callback=on_chunk,
            silence_callback=on_silence,
            max_duration=10
        )

        if audio_data:
            duration = len(audio_data) / (16000 * 2)
            print(f"\n✅ Total audio: {duration:.2f} seconds")
        else:
            print("\n❌ No audio recorded")

    finally:
        recorder.close()
