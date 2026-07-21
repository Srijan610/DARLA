from voice.speaker import speak


def start_darla():
    print("=" * 50)
    print("🤖 DARLA AI Assistant")
    print("=" * 50)

    speak("Hello Srijan.")
    speak("I am DARLA.")
    speak("System initialization complete.")
    speak("How can I assist you today?")


if __name__ == "__main__":
    start_darla()