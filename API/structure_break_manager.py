import json
from openai import OpenAI

from API.open_ai_singleton import OpenAISingleton

memory_categories_explanations = open("memory_categories_explanations.txt", "r").read()  # nopep8
STRUCTURE_BREAKER_SYSTEM_ROLE = """
### Important information ###
- Date format is "DD/MM/YYYY".
- Today's date is {TODAY}.
- Weeks start on Sunday and end on Thursday.
- Weekends start on Friday and end on Saturday.

### System Role ###
You are an expert words analyzer.
You will act as a middleman between a user and an AI personal assistant.
You will get a prompt from the user and analyze it, it will come in the form of >>>>>prompt<<<<<.
The prompt can potentially contain one or more of the following ideas:
- Some personal information about the user's life.
- Some preferences of the user about the AI personal assistant.
- A task for the AI personal assistant to do.

### Output ###
You will analyze the prompt and provide a dictionary with the following structure:
{
    "information": <List of information items - each one is a string>,
    "preferences": <List of preference items - each one is a string>,
    "task": <The task to do - a string>
}

### Personal information instructions ###
- Only extract personal information that fits one of the memory categories provided in the form of !!!!!memory_categories_explanations!!!!!
- If there is no personal information - return an empty list.

### Preferences instructions ###
- The preferences list should contain only the preferences related to the desired behaviour of the AI personal assistant, and not the preferences related to the specific task the user requested.
- If there is no preferences - return an empty list.

### General instructions ###
- Make sure to only use double quotes.
- You must never alter the task or the information in the prompt.
- If there is no task - return an empty string.
"""


def break_structure(prompt: str) -> dict:
    messages = [
        # {"role": "system", "content": f"""Today's date is {TODAY}."""},
        {"role": "system", "content": STRUCTURE_BREAKER_SYSTEM_ROLE},
        {"role": "system", "content": f"!!!!!{memory_categories_explanations}!!!!!"},  # nopep8
        # {"role": "user", "content": EXAMPLE3},
        # {"role": "system", "content": EXAMPLE3_REASONING},  # nopep8
        # # {"role": "assistant", "content": EXAMPLE1_OUTPUT},  # nopep8
        # {"role": "user", "content": EXAMPLE4},
        # {"role": "system", "content": EXAMPLE4_REASONING},  # nopep8
        # # {"role": "assistant", "content": EXAMPLE2_OUTPUT},  # nopep8
        {"role": "user", "content": f">>>>>{prompt}<<<<<"}
    ]

    response = OpenAISingleton().get_response_dict(
        messages=messages,
        temperature=0.33
    )

    return response