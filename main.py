from voice.speaker import speak
from voice.listener import listen


def start_darla():
    print("=" * 50)
    print("🤖 DARLA AI Assistant")
    print("=" * 50)

    speak("Hello Srijan.")
    speak("I am DARLA.")
    speak("System initialization complete.")
    speak("How can I assist you today?")

    while True:
        command = listen()

        if command == "":
            continue

        elif "hello" in command or "good morning" in command:
            speak("Hello Srijan.")

        elif "what is your name" in command or "your name" in command:
            speak("My name is DARLA.")

        elif "who are you" in command:
            speak("I am DARLA, your personal AI assistant.")

        elif "how are you" in command:
            speak("I am functioning perfectly.")

        elif "thank you" in command:
            speak("You're welcome, Srijan.")

        elif "bye" in command or "exit" in command:
            speak("Goodbye Srijan.")
            break

        else:
            speak("I don't know how to answer that yet.")


if __name__ == "__main__":
    start_darla()