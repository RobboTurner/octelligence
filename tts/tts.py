from openai import OpenAI
import pygame
from dotenv import load_dotenv
import os
os.environ['SDL_AUDIODRIVER'] = 'pulse'
pygame.mixer.init(frequency=22050, size=-16, channels=2)


# Load environment variables from .env file
load_dotenv()

def tts(content: str):
    client = OpenAI()

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=content,
    )

    filename = "output.mp3"
    response.stream_to_file(filename)

    # Initialize pygame mixer
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait for the music to play
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

tts('Hello world! This is a text to speech test.')