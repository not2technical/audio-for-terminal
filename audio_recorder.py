"""
Audio recording with Voice Activity Detection (VAD)
"""
import pyaudio
import wave
import webrtcvad
import collections
import array
import time


class AudioRecorder:
    def __init__(
        self,
        sample_rate=16000,
        frame_duration=30,  # ms
        vad_aggressiveness=3  # 0-3, higher = more aggressive
    ):
        self.sample_rate = sample_rate
        self.frame_duration = frame_duration
        self.frame_size = int(sample_rate * frame_duration / 1000)
        self.vad = webrtcvad.Vad(vad_aggressiveness)

        self.audio = pyaudio.PyAudio()
        self.stream = None

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

    def record_until_silence(
        self,
        max_duration=10,
        silence_duration=1.5,
        callback=None
    ):
        """
        Record audio until silence is detected

        Args:
            max_duration: Maximum recording duration in seconds
            silence_duration: Duration of silence to stop recording (seconds)
            callback: Optional callback function called during recording

        Returns:
            bytes: Raw audio data (16-bit PCM)
        """
        self.start_stream()

        frames = []
        voiced_frames = []
        num_silence_frames = int(silence_duration * 1000 / self.frame_duration)
        ring_buffer = collections.deque(maxlen=num_silence_frames)

        triggered = False
        start_time = time.time()

        print("🎤 Recording... (speak now)")

        while time.time() - start_time < max_duration:
            frame = self.stream.read(self.frame_size, exception_on_overflow=False)
            frames.append(frame)

            # Check if frame contains speech
            is_speech = self.vad.is_speech(frame, self.sample_rate)

            if callback:
                callback(is_speech)

            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])

                # Start recording when we detect speech
                if num_voiced > 0.5 * ring_buffer.maxlen:
                    triggered = True
                    print("🗣️  Speech detected, recording...")
                    # Add buffered frames
                    for f, _ in ring_buffer:
                        voiced_frames.append(f)
                    ring_buffer.clear()
            else:
                # Already recording
                voiced_frames.append(frame)
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])

                # Stop recording when silence detected
                if num_unvoiced > 0.9 * ring_buffer.maxlen:
                    print("🤫 Silence detected, stopping...")
                    break

        # If we never detected speech, return empty
        if not triggered:
            print("⚠️  No speech detected")
            return b''

        # Convert frames to bytes
        audio_data = b''.join(voiced_frames)
        return audio_data

    def save_wav(self, audio_data, filename):
        """Save audio data to WAV file"""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data)

    def close(self):
        """Clean up resources"""
        self.stop_stream()
        self.audio.terminate()


# Test the recorder
if __name__ == "__main__":
    recorder = AudioRecorder()

    try:
        print("Say something after the beep...")
        audio_data = recorder.record_until_silence(max_duration=10)

        if audio_data:
            filename = "/tmp/test_recording.wav"
            recorder.save_wav(audio_data, filename)
            print(f"✅ Audio saved to {filename}")
            print(f"   Duration: {len(audio_data) / (16000 * 2):.2f} seconds")
        else:
            print("❌ No audio recorded")

    finally:
        recorder.close()
