from ai.brain import ask_darla
from memory.manager import (
    forget_memory,
    format_memories,
    get_all_memories,
    get_memory,
    save_memory,
)
from voice.listener import listen
from voice.speaker import speak


def clean_memory_statement(statement: str) -> str:
    """Remove unnecessary starting words."""

    statement = statement.strip().lower()

    prefixes = (
        "remember that ",
        "remember ",
        "that ",
    )

    for prefix in prefixes:
        if statement.startswith(prefix):
            statement = statement[len(prefix):].strip()

    return statement


def save_spoken_memory(statement: str) -> bool:
    """Extract and save a memory such as 'my favorite color is black'."""

    statement = clean_memory_statement(statement)

    if " is " not in statement:
        speak(
            "I could not understand the memory. "
            "Please say, my favorite color is black."
        )
        return False

    key, value = statement.split(" is ", 1)

    key = key.strip()
    value = value.strip()

    if not key or not value:
        speak("I could not understand what you wanted me to remember.")
        return False

    save_memory(key, value)

    display_key = key.removeprefix("my ").strip()

    speak(
        f"Got it, Srijan. I will remember that your "
        f"{display_key} is {value}."
    )

    print(f"Memory saved: {display_key} = {value}")
    return True


def handle_remember_command(command: str) -> bool:
    """Handle complete or split remember commands."""

    if not command.startswith("remember"):
        return False

    statement = clean_memory_statement(command)

    # Speech recognition may hear only “remember that”.
    if not statement or " is " not in statement:
        speak("What would you like me to remember?")
        print("Waiting for memory details...")

        details = listen()

        if not details:
            speak("I did not hear the details.")
            return True

        save_spoken_memory(details)
        return True

    save_spoken_memory(statement)
    return True


def handle_recall_command(command: str) -> bool:
    prefixes = (
        "what is my ",
        "what's my ",
        "tell me my ",
        "do you remember my ",
    )

    for prefix in prefixes:
        if command.startswith(prefix):
            key = command[len(prefix):].strip()
            value = get_memory(key)

            if value:
                speak(f"Your {key} is {value}.")
            else:
                speak(f"I do not have a saved memory about your {key}.")

            return True

    return False


def handle_forget_command(command: str) -> bool:
    if not command.startswith("forget"):
        return False

    key = command.removeprefix("forget about").strip()
    key = key.removeprefix("forget").strip()
    key = key.removeprefix("my").strip()

    if not key:
        speak("Please tell me what you want me to forget.")
        return True

    if forget_memory(key):
        speak(f"I have forgotten your {key}.")
    else:
        speak(f"I did not have a saved memory about your {key}.")

    return True


def start_darla() -> None:
    print("=" * 50)
    print("🤖 DARLA AI Assistant")
    print("=" * 50)

    speak("Hello Srijan.")
    speak("I am DARLA.")
    speak("System initialization complete.")
    speak("How can I assist you today?")

    while True:
        command = listen()

        if not command:
            continue

        command = command.lower().strip()

        if "bye" in command or "exit" in command:
            speak("Goodbye Srijan. Have a wonderful day.")
            break

        if "stop listening" in command:
            speak("Stopping now. Goodbye Srijan.")
            break

        if handle_remember_command(command):
            continue

        if handle_forget_command(command):
            continue

        if handle_recall_command(command):
            continue

        if "what do you remember about me" in command:
            memories = get_all_memories()

            if memories:
                summary = ", ".join(
                    f"{key} is {value}"
                    for key, value in memories.items()
                )
                speak(f"I remember that your {summary}.")
            else:
                speak("I have not saved any personal memories yet.")

            continue

        if "what is your name" in command or "who are you" in command:
            speak("My name is DARLA. I am your personal AI assistant.")
            continue

        if "hello" in command or "good morning" in command:
            speak("Hello Srijan. How can I help you?")
            continue

        if "thank you" in command:
            speak("You are welcome, Srijan.")
            continue

        print("DARLA is thinking...")

        answer = ask_darla(
            user_message=command,
            memory_context=format_memories(),
        )

        speak(answer)


if __name__ == "__main__":
    start_darla()