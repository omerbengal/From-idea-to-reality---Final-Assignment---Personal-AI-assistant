from openai import OpenAI
from calendar_handler import *
from memory_handler import *


TODAY = get_now().isoformat()  # nopep8
client = OpenAI(api_key="sk-proj-4YEmICxNrRVUv8OWO3VlT3BlbkFJVbmbwykJsteagH4it3lv")  # nopep8
REQUEST_RELEVANCE_MANAGER_SYSTEM_ROLE = f"""
### Important information ###
- Date format is "DD/MM/YYYY".
- Today's date is {TODAY}.
- Weeks start on Sunday and end on Thursday.
- Weekends start on Friday and end on Saturday.

### System Role ###
You are an expert requests classificator.
You will act as a middleman between a user and an AI personal assistant.
You will get a request that the user whishes the AI assistant would help him with - this request will come in the form of >>>>>request<<<<<.
Your task is to analyze the request and to classify if it is relevant to the AI personal assistant's role or not.

### Request relevance classification ###
The role of the AI personal assistant is to help the user to manage his busy life.
This could be related to the user's tasks and calendar events, life habits, preferences, goals, future plans, interests, hobbies, personality, values, emotions, feelings, thoughts, ideas, and relationships.
Thus, any request that is not related to these areas of knowledge is not relevant to the AI personal assistant's role.

### Memory ###
You will get a dictionary of a memory which contains several aspects of the user's life, This memory will come in the form of !!!!!memory!!!!!.
If the user's request can be answered by data from the memory, then you should output "relevant".

### Output ###
You will ouput a string that is one of 2 possible values:
1. relevant
2. not relevant
"""


def classify_relevance(request: str):

    memory = get_memory()

    messages = [
        # {"role": "system", "content": f"""Today's date is {TODAY}."""},
        {"role": "system", "content": REQUEST_RELEVANCE_MANAGER_SYSTEM_ROLE},
        {"role": "system", "content": f"!!!!!{memory}!!!!!"},  # nopep8
        # {"role": "user", "content": EXAMPLE3},
        # {"role": "system", "content": EXAMPLE3_REASONING},  # nopep8
        # # {"role": "assistant", "content": EXAMPLE1_OUTPUT},  # nopep8
        # {"role": "user", "content": EXAMPLE4},
        # {"role": "system", "content": EXAMPLE4_REASONING},  # nopep8
        # # {"role": "assistant", "content": EXAMPLE2_OUTPUT},  # nopep8
        {"role": "user", "content": f">>>>>{request}<<<<<"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.33,
            seed=42,
        )

        response_message = response.choices[0].message

        return response_message.content if response_message.content else ''

    except Exception as e:
        return f"An error occurred: {str(e)}"
