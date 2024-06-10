from openai import OpenAI
import json
from calendar_handler import *
from tasks_handler import *

client = OpenAI(api_key="sk-proj-4YEmICxNrRVUv8OWO3VlT3BlbkFJVbmbwykJsteagH4it3lv")  # nopep8
SYSTEM_ROLE = """You are a helpful AI personal assistant.
Your main essence is to help the user to manage his busy life.
You will get to know about the user's:
- Tasks and calendar events and will help them to manage them.
- Life, habits, and preferences.
- Goals and Future plans.
- Interests and hobbies.
- Personality and values.
- Emotions and feelings.
- Thoughts and ideas.
- Past experiences and memories.
- Current situation and context.
- Closest relationships and connections.

This could be done in several ways:
- At all times, you could call a function to get the user's schedule and tasks.
- At all times, you could ask the user to provide some information (for example - further information about tasks, calendar events, life habits, etc.).
- At all times, you could ask the user to provide a question or a request.
- You could also use natural language processing to understand the user's intent and provide appropriate responses.

You will always respond in a way that is helpful, kind, and honest to the user.
You will never respond with anything that is not helpful, kind, or honest.

When getting the user's tasks and calendar events, provide them as they are without any modifications or rephrasing.

You can use the following functions:
- get_nearest_saturday(date: datetime) -> datetime: Get the nearest Saturday from a given date.
- get_events_up_to_certain_date(calendarID: str, time_max: datetime) -> list: Get all events from now up to a certain date.
- get_tasks_lists() -> list: Get all tasks lists.
- get_tasks_from_list(tasklistID: str) -> list: Get all tasks from a list.
- get_calendars_IDs() -> list: Get all calendars IDs.
- get_all_tasks() -> list: Get all tasks.
- get_all_uncompleted_tasks() -> list: Get all uncompleted tasks.
"""
FUNCTIONS = [
    {
        "type": "function",
        "function": {
                "name": "get_events_up_to_certain_date",
                "description": "Get all events from now up to a certain date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calendarID": {
                            "type": "string",
                            "description": "The ID of the calendar to get events from."
                        },
                        "time_max": {
                            "type": "string",
                            "format": "date-time",
                            "description": "The maximum date and time to get events up to."
                        }
                    },
                    "required": ["calendarID", "time_max"]
                },
        },
    },
    {
        "type": "function",
        "function": {
                "name": "get_tasks_lists",
                "description": "Get all tasks lists",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
        },
    },
    {
        "type": "function",
        "function": {
                "name": "get_tasks_from_list",
                "description": "Get all tasks from a list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tasklistID": {
                            "type": "string",
                            "description": "The ID of the task list to get tasks from.",
                        },
                    },
                    "required": ["tasklistID"],
                },
        },
    },
    {
        "type": "function",
        "function": {
                "name": "get_calendars_IDs",
                "description": "Get all calendars IDs",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
        },
    },
    {
        "type": "function",
        "function": {
                "name": "get_nearest_saturday",
                "description": "Get the nearest Saturday",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
        },
    },
    {
        "type": "function",
        "function": {
                "name": "get_all_tasks",
                "description": "Get all tasks",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
        },
    },
    {
        "type": "function",
        "function": {
                "name": "get_all_uncompleted_tasks",
                "description": "Get all uncompleted tasks",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
        },
    },
]


def get_nearest_saturday_function():
    """Get the nearest Saturday"""
    nearest_saturday = get_nearest_saturday()
    return json.dumps({"nearest_saturday": nearest_saturday.isoformat()})


def get_events_up_to_certain_date_function(calendarID, time_max):
    """Get all events from now up to a certain date"""
    events = get_events_up_to_certain_date(calendarID, time_max)
    return json.dumps(events)


def get_tasks_lists_function():
    """Get all tasks lists"""
    tasks_lists = get_tasks_lists()
    return json.dumps(tasks_lists)


def get_tasks_from_list_function(tasklistID):
    """Get all tasks from a list"""
    tasks = get_tasks_from_list(tasklistID)
    return json.dumps(tasks)


def get_calendars_IDs_function():
    """Get all calendars IDs"""
    calendars_ids = get_calendars_IDs()
    return json.dumps(calendars_ids)


def get_all_tasks_function():
    """Get all tasks"""
    tasks = get_all_tasks()
    return json.dumps(tasks)


def get_all_uncompleted_tasks_function():
    """Get all uncompleted tasks"""
    tasks = get_all_uncompleted_tasks()
    return json.dumps(tasks)


# def get_response(prompt: str) -> str:
#     messages = [
#         {"role": "system", "content": SYSTEM_ROLE},
#         {"role": "user", "content": prompt}
#     ]

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=messages,
#         tools=FUNCTIONS,
#         tool_choice="auto",
#     )

#     response_message = response.choices[0].message
#     print('first response:', response_message.content)
#     tool_calls = response_message.tool_calls
#     print('tool_calls:', tool_calls)

#     while tool_calls:
#         available_functions = {
#             "get_nearest_saturday": get_nearest_saturday_function,
#             "get_events_up_to_certain_date": get_events_up_to_certain_date_function,
#             "get_tasks_lists": get_tasks_lists_function,
#             "get_tasks_from_list": get_tasks_from_list_function,
#             "get_calendars_IDs": get_calendars_IDs_function,
#             "get_all_tasks": get_all_tasks_function,
#             "get_all_uncompleted_tasks": get_all_uncompleted_tasks_function,
#         }
#         messages.append(response_message)

#         for tool_call in tool_calls:
#             function_name = tool_call.function.name
#             function_to_call = available_functions[function_name]
#             function_args = json.loads(tool_call.function.arguments)
#             function_response = function_to_call(**function_args)
#             messages.append(
#                 {
#                     "tool_call_id": tool_call.id,
#                     "role": "tool",
#                     "name": function_name,
#                     "content": function_response,
#                 }
#             )
#         second_response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=messages,
#             tools=FUNCTIONS,
#             tool_choice="auto",
#         )
#         response_message = second_response.choices[0].message
#         tool_calls = response_message.tool_calls

#     return response_message.content if response_message.content else ''

def get_response(prompt: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_ROLE},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=FUNCTIONS,
            tool_choice="auto",
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        while tool_calls:
            available_functions = {
                "get_nearest_saturday": get_nearest_saturday_function,
                "get_events_up_to_certain_date": get_events_up_to_certain_date_function,
                "get_tasks_lists": get_tasks_lists_function,
                "get_tasks_from_list": get_tasks_from_list_function,
                "get_calendars_IDs": get_calendars_IDs_function,
                "get_all_tasks": get_all_tasks_function,
                "get_all_uncompleted_tasks": get_all_uncompleted_tasks_function,
            }
            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions.get(function_name)
                if function_to_call:
                    function_args = json.loads(tool_call.function.arguments)
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
            )
            response_message = second_response.choices[0].message
            tool_calls = response_message.tool_calls

        return response_message.content if response_message.content else ''

    except Exception as e:
        return f"An error occurred: {str(e)}"
