import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 170)

voices = engine.getProperty("voices")

# Select a female voice if available
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break


def speak(text):
    print(f"DARLA: {text}")
    engine.say(text)
    engine.runAndWait()