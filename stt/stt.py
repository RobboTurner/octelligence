import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

def stt():
    load_dotenv()

    # Set the duration and sample rate
    duration = 3  # seconds
    sample_rate = 16000  # Sample rate in Hertz

    # Record audio from the microphone
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")

    # Save the recorded audio to a WAV file
    wav_file = 'recorded_audio.wav'
    write(wav_file, sample_rate, audio)  # Save as WAV file

    # Initialize OpenAI client
    client = OpenAI()

    # Open the recorded audio file
    with open(wav_file, "rb") as audio_file:
        # Create transcription using the OpenAI API
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )

    # Print the transcription
    return(transcription.text)
