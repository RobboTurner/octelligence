
from dotenv import load_dotenv, dotenv_values
import os 

from openai import OpenAI
import pygame
from dotenv import load_dotenv
import os

def tts(content: str):

    load_dotenv()
    
    client = OpenAI()

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=content,
    )

    filename = "output.mp3"
    response.stream_to_file(filename)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait for the music to play
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

tts('The police in the Northeast have been cut again and again and agin. How do you respond to families who have been the victims of crime and hold you responsible?')
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=content,
    )

    filename = "output.mp3"
    response.stream_to_file(filename)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait for the music to play
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

tts('The police in the Northeast have been cut again and again and agin. How do you respond to families who have been the victims of crime and hold you responsible?')

