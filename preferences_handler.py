import datetime
import json


def get_preferences() -> dict[str, str]:
    with open("preferences.json", "r") as f:
        preferences = json.load(f)
    return preferences


def add_to_preferences(preference_instance: str):
    preferences = get_preferences()

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    preferences[now] = preference_instance

    with open("preferences.json", "w") as f:
        json.dump(preferences, f, indent=4, ensure_ascii=False)


def get_level_of_details_desired() -> int:
    preferences = get_preferences()
    return preferences["level_of_details_desired"]
