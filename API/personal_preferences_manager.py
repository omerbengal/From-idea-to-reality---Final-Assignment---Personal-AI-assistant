from openai import OpenAI

from API.open_ai_singleton import OpenAISingleton
from calendar_handler import *
from preferences_handler import *


TODAY = get_now().isoformat()  # nopep8


client = OpenAI(api_key="sk-proj-4YEmICxNrRVUv8OWO3VlT3BlbkFJVbmbwykJsteagH4it3lv")  # nopep8
PERSONAL_PREFERENCES_MANAGER_SYSTEM_ROLE = """
### Important information ###
- Date format is "DD/MM/YYYY".
- Today's date is {TODAY}.
- Weeks start on Sunday and end on Thursday.
- Weekends start on Friday and end on Saturday.

### System Role ###
You are an expert details analyzer.
You will act as a middleman between a user and an AI personal assistant.
You will get a list of personal preferences of the user about the AI personal assistant - this list will come in the form of >>>>>list<<<<<.
Your task is to analyze the list and insert each preference item to the preferences dictionary if it is not already there.

### General instructions ###
- Make sure to only use double quotes.
- You must never alter the content provided to you, but you can rephrase it a bit to make it more readable.
"""


FUNCTIONS = [
    {
        'type': 'function',
        'function': {
            'name': 'get_preferences',
            'description': 'Get the current preferences dictionary',
            'parameters': {
                'type': 'object',
                'properties': {},
            },
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'add_to_preferences',
            'description': 'Add a string to the preferences dictionary',
            'parameters': {
                'type': 'object',
                'properties': {
                    'preference_instance': {
                        'type': 'string',
                        'description': 'The string to add to the preferences dictionary',
                    },
                },
                'required': ['preference_instance'],
            },
        },
    },
]


def get_preferences_function():
    """Get the current preferences dictionary"""
    preferences = get_preferences()
    return json.dumps(preferences, indent=4, ensure_ascii=False)


def add_to_preferences_function(preference_instance: str):
    """Add a string to the preferences dictionary"""
    add_to_preferences(preference_instance)
    return json.dumps({"success": True}, indent=4, ensure_ascii=False)


def organize_personal_preferences(personal_preferences: list[str]):
    messages = [
        # {"role": "system", "content": f"""Today's date is {TODAY}."""},
        {"role": "system", "content": PERSONAL_PREFERENCES_MANAGER_SYSTEM_ROLE},
        # {"role": "user", "content": EXAMPLE3},
        # {"role": "system", "content": EXAMPLE3_REASONING},  # nopep8
        # # {"role": "assistant", "content": EXAMPLE1_OUTPUT},  # nopep8
        # {"role": "user", "content": EXAMPLE4},
        # {"role": "system", "content": EXAMPLE4_REASONING},  # nopep8
        # # {"role": "assistant", "content": EXAMPLE2_OUTPUT},  # nopep8
        {"role": "user", "content": f">>>>>{personal_preferences}<<<<<"}
    ]

    available_functions = {
        "get_preferences": get_preferences_function,
        "add_to_preferences": add_to_preferences_function,
    }

    response = OpenAISingleton().get_response_with_function_calling(
        messages=messages,
        functions=FUNCTIONS,
        available_functions=available_functions,
        temperature=0.25
    )

    return response
