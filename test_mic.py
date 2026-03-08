#!/usr/bin/env python3
"""
Quick microphone test - verifies audio input is working
"""
import pyaudio
import sys

print("\n" + "="*60)
print("🎤 Microphone Test")
print("="*60 + "\n")

try:
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    print("📋 Available audio devices:\n")

    # List all audio devices
    info = audio.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    input_devices = []
    for i in range(num_devices):
        device_info = audio.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            input_devices.append(device_info)
            print(f"   [{i}] {device_info.get('name')}")
            print(f"       Channels: {device_info.get('maxInputChannels')}")
            print(f"       Sample Rate: {int(device_info.get('defaultSampleRate'))} Hz")
            print()

    if not input_devices:
        print("❌ No input devices found!")
        sys.exit(1)

    print("="*60)
    print("✅ Microphone access working!")
    print("="*60)
    print(f"\nFound {len(input_devices)} input device(s)")
    print("\n💡 Tip: macOS may prompt for microphone permissions")
    print("   on first run. Click 'Allow' to proceed.\n")

    audio.terminate()

except Exception as e:
    print(f"\n❌ Error: {e}\n")
    print("💡 Make sure you've granted microphone permissions:")
    print("   System Settings → Privacy & Security → Microphone\n")
    sys.exit(1)
