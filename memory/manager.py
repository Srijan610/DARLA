import json
from pathlib import Path
from typing import Any


MEMORY_FILE = Path(__file__).with_name("memory.json")


def _load_memory() -> dict[str, Any]:
    """Load all saved memories."""

    if not MEMORY_FILE.exists():
        MEMORY_FILE.write_text("{}", encoding="utf-8")

    try:
        content = MEMORY_FILE.read_text(encoding="utf-8").strip()

        if not content:
            return {}

        data = json.loads(content)

        if isinstance(data, dict):
            return data

    except (json.JSONDecodeError, OSError) as error:
        print(f"Memory loading error: {error}")

    return {}


def _save_all(memory: dict[str, Any]) -> None:
    """Save all memories to disk."""

    MEMORY_FILE.write_text(
        json.dumps(memory, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )


def normalize_key(key: str) -> str:
    """Normalize keys so equivalent phrases match."""

    key = key.strip().lower().rstrip("?.!")

    replacements = {
        "colour": "color",
        "favourite": "favorite",
        "girlfriend's": "girlfriend",
        "girlfriends": "girlfriend",
        "what is": "",
        "what's": "",
    }

    for old, new in replacements.items():
        key = key.replace(old, new)

    prefixes = (
        "remember that ",
        "remember ",
        "tell me my ",
        "do you remember my ",
        "my ",
        "the ",
    )

    for prefix in prefixes:
        if key.startswith(prefix):
            key = key[len(prefix):]

    return " ".join(key.split())


def save_memory(key: str, value: str) -> None:
    memory = _load_memory()
    memory[normalize_key(key)] = value.strip().rstrip(".")
    _save_all(memory)


def get_memory(key: str) -> str | None:
    memory = _load_memory()
    normalized_key = normalize_key(key)

    if normalized_key in memory:
        return str(memory[normalized_key])

    for saved_key, saved_value in memory.items():
        if normalized_key in saved_key or saved_key in normalized_key:
            return str(saved_value)

    return None


def forget_memory(key: str) -> bool:
    memory = _load_memory()
    normalized_key = normalize_key(key)

    if normalized_key in memory:
        del memory[normalized_key]
        _save_all(memory)
        return True

    return False


def get_all_memories() -> dict[str, Any]:
    return _load_memory()


def format_memories() -> str:
    memory = _load_memory()

    if not memory:
        return "No personal memories have been saved yet."

    return "\n".join(
        f"- {key}: {value}"
        for key, value in memory.items()
    )