import datetime
import json


def get_memory() -> dict[str, str]:
    with open("memory.json", "r") as f:
        memory = json.load(f)
    return memory


def add_to_memory(category: str, memory_instance: str):
    memory = get_memory()

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    memory[category][now] = memory_instance

    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)


def get_memory_categories() -> list[str]:
    memory = get_memory()
    return list(memory.keys())


def add_memory_category(category: str):
    memory = get_memory()

    if category not in memory:
        memory[category] = {}
        with open("memory.json", "w") as f:
            json.dump(memory, f, indent=4, ensure_ascii=False)
