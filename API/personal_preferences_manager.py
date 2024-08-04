from openai import OpenAI
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

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=FUNCTIONS,
            tool_choice="auto",
            temperature=0.33,
            seed=42,
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        counter = 0
        while tool_calls:
            counter += 1
            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions.get(function_name)
                if function_to_call:
                    function_args = json.loads(tool_call.function.arguments)
                    print(f"({counter}) calling function {function_name}, with args {function_args}")  # nopep8
                    try:
                        function_response = function_to_call(**function_args)
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": function_response,
                            }
                        )
                    except Exception as e:
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": json.dumps({"error": str(e)}),
                            }
                        )
            second_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=FUNCTIONS,
                tool_choice="auto",
                temperature=0.33,
                seed=42,
            )
            response_message = second_response.choices[0].message
            tool_calls = response_message.tool_calls

        return response_message.content if response_message.content else ''

    except Exception as e:
        return f"An error occurred: {str(e)}"
