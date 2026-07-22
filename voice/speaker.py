import asyncio
import edge_tts
from playsound import playsound
import os
import uuid

VOICE = "en-US-AriaNeural"

async def generate_voice(text, filename):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)

def speak(text):
    print(f"DARLA: {text}")

    filename = f"{uuid.uuid4()}.mp3"

    asyncio.run(generate_voice(text, filename))

    playsound(filename)

    os.remove(filename)