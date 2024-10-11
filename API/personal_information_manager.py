from openai import OpenAI

from open_ai_singleton import OpenAISingleton
from calendar_handler import *
from memory_handler import *


TODAY = get_now().isoformat()
client = OpenAI(api_key="sk-proj-4YEmICxNrRVUv8OWO3VlT3BlbkFJVbmbwykJsteagH4it3lv")
memory_categories_explanations = open("memory_categories_explanations.txt", "r").read()
PERSONAL_INFORMATION_MANAGER_SYSTEM_ROLE = f"""
### Important information ###
- Date format is "DD/MM/YYYY".
- Today's date is {TODAY}.
- Weeks start on Sunday and end on Thursday.
- Weekends start on Friday and end on Saturday.

### System Role ###
You are an expert details analyzer.
You will act as a middleman between a user and an AI personal assistant.
You will get a list of personal information about the user's life - this list will come in the form of >>>>>list<<<<<.
Your task is to analyze the list and insert each information item in the best suitable category in the memory if it is not already there.

### Personal information classification ###
You will get a description for each available category.
This description will come in the form of !!!!!category_description!!!!!.
You should use this explanation to classify the information you get from the user.

### General instructions ###
- Make sure to only use double quotes.
- You must never alter the content provided to you, but you can rephrase it a bit to make it more readable.
- The insformation list should contain only personal information of the user, and not temporary information related to the specific task the user requested.
- If a piece of information (or a part of it) already exists in the memory, do not add it again, but instead update the existing information.
"""


FUNCTIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_memory",
            "description": "Get the current memory dictionary",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_memory",
            "description": "Add a string to the memory dictionary",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The category to add the string to",
                    },
                    "memory_instance": {
                        "type": "string",
                        "description": "The string to add to the memory dicitonary",
                    },
                },
                "required": ["category", "memory_instance"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_memory_categories",
            "description": "Get all categories in the memory dictionary",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]


def get_memory_function():
    """Get the current memory dictionary"""
    memory = get_memory()
    return json.dumps(memory, indent=4, ensure_ascii=False)


def add_to_memory_function(category: str, memory_instance: str):
    """Add a string to the memory dictionary"""
    add_to_memory(category, memory_instance)
    return json.dumps({"success": True}, indent=4, ensure_ascii=False)


def get_memory_categories_function():
    """Get all categories in the memory dictionary"""
    categories = get_memory_categories()
    return json.dumps(categories, indent=4, ensure_ascii=False)


def organize_personal_information(personal_information: list[str]):
    messages = [
        # {"role": "system", "content": f"""Today's date is {TODAY}."""},
        {"role": "system", "content": PERSONAL_INFORMATION_MANAGER_SYSTEM_ROLE},
        {"role": "system", "content": f"!!!!!{memory_categories_explanations}!!!!!"},
        # {"role": "user", "content": EXAMPLE3},
        # {"role": "system", "content": EXAMPLE3_REASONING},
        # # {"role": "assistant", "content": EXAMPLE1_OUTPUT},
        # {"role": "user", "content": EXAMPLE4},
        # {"role": "system", "content": EXAMPLE4_REASONING},
        # # {"role": "assistant", "content": EXAMPLE2_OUTPUT},
        {"role": "user", "content": f">>>>>{personal_information}<<<<<"}
    ]

    available_functions = {
        "get_memory": get_memory_function,
        "add_to_memory": add_to_memory_function,
        "get_memory_categories": get_memory_categories_function,
    }

    response = OpenAISingleton().get_response_with_function_calling(
        messages=messages,
        functions=FUNCTIONS,
        available_functions=available_functions,
        temperature=0.25
    )

    return response
