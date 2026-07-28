import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY was not found. Check your .env file."
    )


client = genai.Client(api_key=api_key)


def ask_darla(user_message: str, memory_context: str = "") -> str:
    """Send a message and relevant memories to Gemini."""

    if not user_message or not user_message.strip():
        return "I did not receive a question, Srijan."

    system_instruction = (
        "You are DARLA, Srijan's personal AI assistant. "
        "Your name is DARLA. Always address the user as Srijan. "
        "Answer warmly, clearly, and briefly because your response "
        "will be spoken aloud. Do not use markdown, headings, bullet "
        "points, emojis, or special formatting. Keep ordinary answers "
        "under four sentences."
    )

    if memory_context:
        system_instruction += (
            "\n\nThese are DARLA's saved personal memories about Srijan:\n"
            f"{memory_context}\n"
            "Use these memories only when they are relevant. "
            "Do not invent memories that are not listed."
        )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=500,
            ),
        )

        answer = response.text

        if not answer:
            return "Sorry Srijan, I could not form an answer."

        return answer.strip()

    except Exception as error:
        print(f"Gemini error: {error}")
        return "Sorry Srijan, I could not connect to my AI brain."