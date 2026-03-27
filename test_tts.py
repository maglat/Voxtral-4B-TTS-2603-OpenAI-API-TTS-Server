#!/usr/bin/env python3
"""
Test script for Voxtral TTS with OpenAI-compatible API.
Tests text-to-speech generation and optionally verifies with STT.
"""

import io
import os
import httpx
import soundfile as sf
import argparse

BASE_URL = os.getenv("TTS_BASE_URL", "http://localhost:4576/v1")
STT_URL = os.getenv("STT_URL", "http://192.168.178.5:8083/v1/audio/transcriptions")

def generate_speech(text: str, voice: str = "de_female", output_file: str = "/tmp/audio.wav", response_format: str = "wav"):
    """Generate speech from text using Voxtral TTS."""
    payload = {
        "input": text,
        "model": "mistralai/Voxtral-4B-TTS-2603",
        "response_format": response_format,
        "voice": voice,
    }

    print(f"Generating speech: '{text}'")
    print(f"Voice: {voice}, Format: {response_format}")

    response = httpx.post(f"{BASE_URL}/audio/speech", json=payload, timeout=120.0)
    response.raise_for_status()

    with open(output_file, "wb") as f:
        f.write(response.content)

    print(f"Audio saved to: {output_file}")
    return output_file

def verify_with_stt(audio_file: str):
    """Verify generated audio by transcribing it with STT server."""
    print(f"\nVerifying audio with STT server at {STT_URL}...")

    with open(audio_file, "rb") as f:
        files = {"file": f}
        response = httpx.post(STT_URL, files=files, timeout=60.0)

    if response.status_code == 200:
        result = response.json()
        transcription = result.get("text", "No text in response")
        print(f"STT Transcription: '{transcription}'")
        return transcription
    else:
        print(f"STT request failed with status {response.status_code}")
        return None

def list_voices():
    """List available voices from the TTS server."""
    try:
        response = httpx.get(f"{BASE_URL}/audio/voices", timeout=10.0)
        response.raise_for_status()
        voices = response.json()
        print("\nAvailable voices:")
        for voice in voices.get("voices", []):
            print(f"  - {voice}")
        return voices
    except Exception as e:
        print(f"Could not fetch voices: {e}")
        return None

def check_server_health():
    """Check if the TTS server is running."""
    try:
        response = httpx.get(f"{BASE_URL.replace('/v1', '')}/health", timeout=5.0)
        return response.status_code == 200
    except Exception:
        return False

def main():
    parser = argparse.ArgumentParser(description="Test Voxtral TTS API")
    parser.add_argument("--text", "-t", default="Hallo, das ist ein Test.", help="Text to convert to speech")
    parser.add_argument("--voice", "-v", default="de_female", help="Voice to use (e.g., de_female, de_male)")
    parser.add_argument("--output", "-o", default="/tmp/audio.wav", help="Output audio file")
    parser.add_argument("--format", "-f", default="wav", choices=["wav", "mp3", "flac", "opus", "pcm"], help="Audio format")
    parser.add_argument("--verify", "-V", action="store_true", help="Verify audio with STT server")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    parser.add_argument("--check", "-c", action="store_true", help="Check server health only")

    args = parser.parse_args()

    # Check server health
    if not check_server_health():
        print("ERROR: TTS server is not running at http://localhost:4576")
        print("Start the server with: docker-compose up")
        return 1

    print("TTS server is running!")

    if args.list_voices:
        list_voices()
        return 0

    # Generate speech
    generate_speech(args.text, args.voice, args.output, args.format)

    # Verify with STT if requested
    if args.verify:
        transcription = verify_with_stt(args.output)
        if transcription:
            print(f"\nOriginal:  '{args.text}'")
            print(f"Transcribed: '{transcription}'")

    return 0

if __name__ == "__main__":
    exit(main())
