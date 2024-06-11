from openai import OpenAI
import json
from calendar_handler import *
from tasks_handler import *

TODAY = get_now().isoformat()

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

Important information:
- Today is {TODAY}.
- When getting the user's tasks and calendar events, you can restructure them as you see fit, but in any case - do not modify the name or description of the events or tasks. Even if the user asked for a summary of the tasks, you should not modify the name or description of the events, calendars, lists, or tasks.
- Weekends are considered to be Friday and Saturday.

You can use the following functions:
- get_nearest_saturday(date: datetime = datetime.datetime.now(datetime.timezone.utc)) -> datetime: Get the next nearest Saturday to a given date (default is today).
- get_all_events_from_specific_calendar_up_to_certain_date(calendarID: str, time_max: datetime) -> list[dict]: Get all events from now up to a certain date from a given calendar.
- get_all_events_from_all_calendars_up_to_certain_date(time_max: datetime) -> dict[str, list[dict]]: Get all events from all calendars up to a certain date.
- get_all_calendars_data() -> list[str]: Get all calendars data, including their IDs and summary.
- get_all_tasks_lists() -> list: Get all tasks lists.
- get_all_tasks_from_list(tasklistID: str) -> list: Get all tasks from a given list.
- get_all_tasks() -> dict[str, list]: Get all tasks, organized by lists.
- get_all_uncompleted_tasks() -> dict[str, list]: Get all uncompleted tasks, organized by lists.
"""
FUNCTIONS = [
    {
        "type": "function",
        "function": {
                "name": "get_nearest_saturday",
                "description": "Get the next nearest Saturday to a given date (default is today)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "format": "date-time",
                            "description": "The date to get the nearest Saturday to (default is today)."
                        }
                    },
                }
        }
    },
    {
        "type": "function",
        "function": {
                "name": "get_all_events_from_specific_calendar_up_to_certain_date",
                "description": "Get all events from now up to a certain date from a given calendar",
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
                "name": "get_all_events_from_all_calendars_up_to_certain_date",
                "description": "Get all events from all calendars up to a certain date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "time_max": {
                            "type": "string",
                            "format": "date-time",
                            "description": "The maximum date and time to get events up to."
                        }
                    },
                    "required": ["time_max"]
                },
        },
    },
    {
        "type": "function",
        "function": {
                "name": "get_all_calendars_data",
                "description": "Get all calendars data, including their IDs and summary",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
        },
    },
    {
        "type": "function",
        "function": {
                "name": "get_all_tasks_lists",
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
                "name": "get_all_tasks_from_list",
                "description": "Get all tasks from a given list",
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
                "name": "get_all_tasks",
                "description": "Get all tasks, organized by lists",
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
                "description": "Get all uncompleted tasks, organized by lists",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
        },
    },
]


def get_nearest_saturday_function(date: datetime = datetime.datetime.now(datetime.timezone.utc)):
    """Get the nearest Saturday"""
    nearest_saturday = get_nearest_saturday(date)
    return json.dumps({"nearest_saturday": nearest_saturday.isoformat()})


def get_all_events_from_specific_calendar_up_to_certain_date_function(calendarID, time_max):
    """Get all events from now up to a certain date"""
    events = get_all_events_from_specific_calendar_up_to_certain_date(calendarID, time_max)  # nopep8
    return json.dumps(events, indent=4, ensure_ascii=False)


def get_all_events_from_all_calendars_up_to_certain_date_function(time_max):
    """Get all events from all calendars up to a certain date"""
    events = get_all_events_from_all_calendars_up_to_certain_date(time_max)  # nopep8
    return json.dumps(events, indent=4, ensure_ascii=False)


def get_all_calendars_data_function():
    """Get all calendars data, including their IDs and summary"""
    calendars_data = get_all_calendars_data()
    return json.dumps(calendars_data, indent=4, ensure_ascii=False)


def get_all_tasks_lists_function():
    """Get all tasks lists"""
    tasks_lists = get_all_tasks_lists()
    return json.dumps(tasks_lists, indent=4, ensure_ascii=False)


def get_all_tasks_from_list_function(tasklistID):
    """Get all tasks from a list"""
    tasks = get_all_tasks_from_list(tasklistID)
    return json.dumps(tasks, indent=4, ensure_ascii=False)


def get_all_tasks_function():
    """Get all tasks, organized by lists"""
    tasks = get_all_tasks()
    return json.dumps(tasks, indent=4, ensure_ascii=False)


def get_all_uncompleted_tasks_function():
    """Get all uncompleted tasks, organized by lists"""
    tasks = get_all_uncompleted_tasks()
    print(f"uncompleted tasks: {json.dumps(tasks, indent=4, ensure_ascii=False)}")  # nopep8
    return json.dumps(tasks, indent=4, ensure_ascii=False)


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
    print(f"today is {TODAY}")
    messages = [
        {"role": "system", "content": SYSTEM_ROLE},
        {"role": "user", "content": prompt}
    ]

    available_functions = {
        "get_nearest_saturday": get_nearest_saturday_function,
        "get_all_events_from_specific_calendar_up_to_certain_date": get_all_events_from_specific_calendar_up_to_certain_date_function,
        "get_all_events_from_all_calendars_up_to_certain_date": get_all_events_from_all_calendars_up_to_certain_date_function,
        "get_all_calendars_data": get_all_calendars_data_function,
        "get_all_tasks_lists": get_all_tasks_lists_function,
        "get_all_tasks_from_list": get_all_tasks_from_list_function,
        "get_all_tasks": get_all_tasks_function,
        "get_all_uncompleted_tasks": get_all_uncompleted_tasks_function,
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=FUNCTIONS,
            tool_choice="auto",
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        print(f"checking if need to use tools")
        counter = 0
        while tool_calls:
            counter += 1
            print(f"I'm using tools now! ({counter})")
            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
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
            )
            response_message = second_response.choices[0].message
            tool_calls = response_message.tool_calls

        return response_message.content if response_message.content else ''

    except Exception as e:
        return f"An error occurred: {str(e)}"
