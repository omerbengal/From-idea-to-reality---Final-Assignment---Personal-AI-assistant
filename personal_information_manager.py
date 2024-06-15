from openai import OpenAI
from calendar_handler import *
from memory_handler import *


TODAY = get_now().isoformat()  # nopep8


client = OpenAI(api_key="sk-proj-4YEmICxNrRVUv8OWO3VlT3BlbkFJVbmbwykJsteagH4it3lv")  # nopep8
PERSONAL_INFORMATION_MANAGER_SYSTEM_ROLE = f"""
### Important information ###
- Date format is "DD/MM/YYYY".
- Today's date is {TODAY}.
- Weeks starts on Sunday and ends on Thursday.
- Weekends starts on Friday and ends on Saturday.

### System Role ###
You are an expert details analyzer.
You will act as a middleman between a user and an AI personal assistant.
You will get a list of personal information about the user's life - this list will come in the form of >>>>>list<<<<<.
Your task is to analyze the list and insert each information item in the best suitable category in the memory if it is not already there.

### General instructions ###
- Make sure to only use double quotes.
- You must never alter the content provided to you, but you can rephrase it a bit to make it more readable.
- The insformation list should contain only personal information of the user, and not temporary information related to the specific task the user requested.
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
        # {"role": "user", "content": EXAMPLE3},
        # {"role": "system", "content": EXAMPLE3_REASONING},  # nopep8
        # # {"role": "assistant", "content": EXAMPLE1_OUTPUT},  # nopep8
        # {"role": "user", "content": EXAMPLE4},
        # {"role": "system", "content": EXAMPLE4_REASONING},  # nopep8
        # # {"role": "assistant", "content": EXAMPLE2_OUTPUT},  # nopep8
        {"role": "user", "content": f">>>>>{personal_information}<<<<<"}
    ]

    available_functions = {
        "get_memory": get_memory_function,
        "add_to_memory": add_to_memory_function,
        "get_memory_categories": get_memory_categories_function,
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

        print(f"checking if need to use tools")
        counter = 0
        while tool_calls:
            counter += 1
            print(f"I'm using tools now! ({counter})")
            messages.append(response_message)

            print(f"going through tool calls! ({counter}):\n{tool_calls}")
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                print(f"function name: {function_name} ({counter})")
                function_to_call = available_functions.get(function_name)
                if function_to_call:
                    function_args = json.loads(tool_call.function.arguments)
                    print(f"{counter} - calling function {function_name}, with args {function_args}")  # nopep8
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
