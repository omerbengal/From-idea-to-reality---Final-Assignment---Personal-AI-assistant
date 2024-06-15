import json
from openai import OpenAI


client = OpenAI(api_key="sk-proj-4YEmICxNrRVUv8OWO3VlT3BlbkFJVbmbwykJsteagH4it3lv")  # nopep8
STRUCTURE_BREAKER_SYSTEM_ROLE = """
### Important information ###
- Date format is "DD/MM/YYYY".
- Today's date is {TODAY}.
- Weeks starts on Sunday and ends on Thursday.
- Weekends starts on Friday and ends on Saturday.

### System Role ###
You are an expert words analyzer.
You will act as a middleman between a user and an AI personal assistant.
You will get a prompt from the user and analyze it, it will come in the form of >>>>>prompt<<<<<.
The prompt can potentially contian one or more of the following ideas:
- Some personal information about the user's life.
- Some preferences of the user about the AI personal assistant.
- A task for the AI personal assistant to do.

### Output ###
You will analyze the prompt and provide a dictionary with the following structure:
{
    "information": <List of information items - each one is a string>,
    "preferences": <List of preference items - each one is a string>,
    "task": <The task to do - a string>}
}

### General instructions ###
- Make sure to only use double quotes.
- You must never alter the task or the information in the prompt.
- The preferences list should contain only the preferences related to the desired behaviour of the AI personal assistant, and not the preferences related to the specific task the user requested.
"""


def break_structure(prompt: str) -> dict:
    messages = [
        # {"role": "system", "content": f"""Today's date is {TODAY}."""},
        {"role": "system", "content": STRUCTURE_BREAKER_SYSTEM_ROLE},
        # {"role": "user", "content": EXAMPLE3},
        # {"role": "system", "content": EXAMPLE3_REASONING},  # nopep8
        # # {"role": "assistant", "content": EXAMPLE1_OUTPUT},  # nopep8
        # {"role": "user", "content": EXAMPLE4},
        # {"role": "system", "content": EXAMPLE4_REASONING},  # nopep8
        # # {"role": "assistant", "content": EXAMPLE2_OUTPUT},  # nopep8
        {"role": "user", "content": f">>>>>{prompt}<<<<<"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.33,
            seed=42,
        )

        response_message = response.choices[0].message

        return json.loads(response_message.content) if response_message.content else ''

    except Exception as e:
        return f"An error occurred: {str(e)}"
